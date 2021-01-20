from comet_ml import Experiment

import argparse
import os
from os.path import join, dirname
import time
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import torch
import torch.distributions.constraints as constraints
from tqdm import tqdm

import boto3
import ids_data
import pyro
import pyro.distributions as dist
from botocore.exceptions import ClientError
from pyro.infer import SVI, JitTraceEnum_ELBO, TraceEnum_ELBO, config_enumerate
from pyro.optim import Adam
from slack_notificater import SlackNotificater

plt.style.use('seaborn')
torch.set_num_threads(32)
torch.set_num_interop_threads(32)

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@config_enumerate
def model(data=None, args=None):
    alpha = torch.ones(args['G'])
    theta = pyro.sample('theta', dist.Dirichlet(alpha))

    with pyro.plate('group', args['G']):
        gamma = torch.ones(args['U'])
        kappa = torch.ones(args['T'])
        beta = torch.ones(args['L'])
        delta = torch.ones(args['W'])
        pi = pyro.sample('pi', dist.Dirichlet(gamma))
        tau = pyro.sample('tau', dist.Dirichlet(kappa))
        phi = pyro.sample('phi', dist.Dirichlet(beta))
        sigma = pyro.sample('sigma', dist.Dirichlet(delta))

    with pyro.plate('location', args['L']):
        zeta = torch.ones(3)
        epsilon = torch.ones(args['W'])
        eta = pyro.sample('eta', dist.Dirichlet(zeta))
        mu = pyro.sample('mu', dist.Dirichlet(epsilon))

    with pyro.plate('time', args['T']):
        iota = torch.ones(args['W'])
        rho = pyro.sample('rho', dist.Dirichlet(iota))

    with pyro.plate('data', args['R']) as ind:
        g = pyro.sample('g_{}'.format(ind), dist.Categorical(theta))
        pyro.sample('u_{}'.format(ind), dist.Categorical(pi[g]), obs=data['u'][ind])
        t = pyro.sample('t_{}'.format(ind), dist.Categorical(tau[g]), obs=data['t'][ind])
        l = pyro.sample('l_{}'.format(ind), dist.Categorical(phi[g]), obs=data['l'][ind])

        lmd = pyro.sample('lambda_{}'.format(ind), dist.Multinomial(1, eta[l]))
        with pyro.plate('tag_plate_{}'.format(ind), args['lenW']):
            pyro.sample('tag_{}'.format(ind), 
                dist.Categorical(
                    lmd.index_select(1, torch.LongTensor([0])) * mu[l] 
                    + lmd.index_select(1, torch.LongTensor([1])) * rho[t] 
                    + lmd.index_select(1, torch.LongTensor([2])) * sigma[g]
                ), 
                obs=data['tag'].index_select(1, ind)
            )

@config_enumerate
def guide(data=None, args=None):
    alpha_q = pyro.param('alpha_q', torch.ones(args['G']), constraint=constraints.positive)
    theta = pyro.sample('theta', dist.Dirichlet(alpha_q))

    gamma_q = pyro.param('gamma_q', torch.ones(args['G'], args['U']), constraint=constraints.positive)
    kappa_q = pyro.param('kappa_q', torch.ones(args['G'], args['T']), constraint=constraints.positive)
    beta_q = pyro.param('beta_q', torch.ones(args['G'], args['L']), constraint=constraints.positive)
    delta_q = pyro.param('delta_q', torch.ones(args['G'], args['W']), constraint=constraints.positive)
    with pyro.plate('group', args['G']):
        pi = pyro.sample('pi', dist.Dirichlet(gamma_q))
        tau = pyro.sample('tau', dist.Dirichlet(kappa_q))
        phi = pyro.sample('phi', dist.Dirichlet(beta_q))
        sigma = pyro.sample('sigma', dist.Dirichlet(delta_q))

    zeta_q = pyro.param('zeta_q', torch.ones(args['L'], 3), constraint=constraints.positive)
    epsilon_q = pyro.param('epsilon_q', torch.ones(args['L'], args['W']), constraint=constraints.positive)
    with pyro.plate('location', args['L']):
        eta = pyro.sample('eta', dist.Dirichlet(zeta_q))
        mu = pyro.sample('mu', dist.Dirichlet(epsilon_q))

    iota_q = pyro.param('iota_q', torch.ones(args['T'], args['W']), constraint=constraints.positive)
    with pyro.plate('time', args['T']):
        rho = pyro.sample('rho', dist.Dirichlet(iota_q))

    g_q = pyro.param('g_q', torch.ones(args['R'], args['G']), constraint=constraints.positive)
    lambda_q = pyro.param('lambda_q', torch.ones(args['R'], 3), constraint=constraints.positive)
    with pyro.plate('data', args['R'], subsample_size=int(args['R'] / 5)) as ind:
        g = pyro.sample('g_{}'.format(ind), dist.Categorical(g_q.index_select(0, ind)))
        lmd = pyro.sample('lambda_{}'.format(ind), dist.Multinomial(1, lambda_q.index_select(0, ind)))

    return theta, pi, tau, phi, sigma, eta, mu, rho, g, lmd

def save_posterior(filename, ids):
    posterior_dic = {}
    for name in pyro.get_param_store():
        posterior_dic[name] = pyro.param(name)

    posterior_dic['test_ids'] = ids.test_ids
    posterior_dic['data_file'] = ids.filename

    torch.save(posterior_dic, filename)
    upload_s3(filename)

def upload_s3(file_name):
    session = boto3.Session(profile_name=os.environ.get('AWS_PROFILE'))
    s3 = session.client('s3')
    bucket_name = os.environ.get('AWS_BUCKET')

    try:
        _ = s3.upload_file(file_name, bucket_name, file_name)

        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print('Could not remove: ', file_name)
    except ClientError as e:
        print(e)

def notificate_slack(args, data_file_name):
    sn = SlackNotificater()

    data = {
        'blocks': [
            sn.markdown_block(':fire: SVI Optimization has finished :fire:\n' + args.description),
            sn.divider_block(),
            sn.markdown_block(':bulb: *Execution Information* :bulb:'),
            sn.multiple_field_block([
                sn.markdown_field('*Execution File*\n' + __file__),
                sn.markdown_field('*Hostname*\n' + os.uname()[1]),
                sn.markdown_field('*Input File*\n' + data_file_name),
            ]),
            sn.divider_block(),
            sn.markdown_block(':comet: *Comet Project* :comet:\n' + '<https://www.comet.ml/' + os.environ.get('COMET_WORKSPACE') + '/' + os.environ.get('COMET_PROJECT') + '|click here>'),
        ]
    }

    sn.send_slack_request(data)

def notificate_error(data_file_name, train_ratio, error_desc):
    sn = SlackNotificater()

    data = {
        'blocks': [
            sn.markdown_block(':warning: Experiment failed ! :warning:\n'),
            sn.divider_block(),
            sn.markdown_block(':bulb: *Execution Information* :bulb:'),
            sn.multiple_field_block([
                sn.markdown_field('*Input File*\n' + data_file_name),
                sn.markdown_field('*Train Ratio*\n' + str(train_ratio))
            ]),
            sn.markdown_block('*Error Description*\n' + error_desc),
            sn.divider_block(),
            sn.markdown_block(':comet: *Comet Project* :comet:\n' + '<https://www.comet.ml/' + os.environ.get('COMET_WORKSPACE') + '/' + os.environ.get('COMET_PROJECT') + '|click here>'),
        ]
    }

    sn.send_slack_request(data)

def run(args, group_count, step_count, data_file_name, train_ratio=0.8):
    if args.debug:
        experiment = Experiment(
                api_key=os.environ.get('COMET_API_KEY'),
                project_name="test",
                workspace=os.environ.get('COMET_WORKSPACE'),
                auto_output_logging='simple')
    else:
        experiment = Experiment(
                api_key=os.environ.get('COMET_API_KEY'),
                project_name=os.environ.get('COMET_PROJECT'),
                workspace=os.environ.get('COMET_WORKSPACE'),
                auto_output_logging='simple')

    hyper_params = {
            'group_count': group_count,
            'train_ratio': train_ratio,
            }
    adam_param = {'lr': 0.001, 'betas': (0.95, 0.999)}
    hyper_params.update(adam_param)
    hyper_params.update(vars(args))

    experiment.set_cmd_args()
    experiment.add_tag('st')
    experiment.log_dataset_info(path=data_file_name)
    experiment.log_parameters(hyper_params)

    print('Collecting data....')
    ids_data_in = ids_data.IdsData(data_file_name, group_count)
    ids_data_in.divide_dataset(ratio=train_ratio)
    data, vi_args = ids_data_in.get_training_set()
    print('Collecting data done')

    print('Optimizing....')
    start = time.time()
    optimizer = Adam(adam_param)

    pyro.clear_param_store()
    svi = SVI(model, guide, optimizer, loss=TraceEnum_ELBO(max_plate_nesting=2))

    with experiment.train():
        losses = []
        n_steps = step_count # args.num_step
        for step in tqdm(range(n_steps)):
            loss = svi.step(data, vi_args)
            losses.append(loss)
            experiment.log_metric('loss', loss, step=step)

    duration = time.time() - start
    experiment.log_metric('duration', duration)
    print('Optimizing done.')

    print('Saving data...')
    save_posterior(experiment.get_key() + '.pkl', ids_data_in)
    print('Saving data done.')

    experiment.end()

def main(args):
    print(args)
    data_file_prefix = './data/ids/id-'

    cities = {
            "Buda-allPOI": 10000, # 16997 data
            "Delh-allPOI": 5000, # 3361 data
            "Edin": 12000, # 30495 data
            "Glas": 7000, # 10289 data
            "Osak": 7000, # 7028 data
            "Pert-allPOI": 5000, # 2404 data
            "Toro": 12000, # 32351 data
            "Vien-allPOI": 12000, # 29614 data
            }
    train_ratios = [0.2, 0.5, 0.8]

    if args.debug:
        run(args, 3, 100, data_file_prefix + "Pert-allPOI" + ".csv")
    else:
        group_count = 10

        for city, step_count in cities.items():
            data_file_name = data_file_prefix + city + '.csv'
            for ratio in train_ratios:
                try:
                    run(args, group_count, step_count, data_file_name, ratio)
                except Exception as err:
                    notificate_error(data_file_name, ratio, repr(err))
            notificate_slack(args, data_file_name)


if __name__ == '__main__':
    assert pyro.__version__.startswith('1.3.1')
    pyro.enable_validation()
    parser = argparse.ArgumentParser(description='pyro model using SVI')
    parser.add_argument('--num-experiments', nargs='?', default=1, type=int,
            help='the number of experiments for the same situation')
    parser.add_argument('--debug', action='store_true', 
            help='debug mode (not notificate_to_slack)')
    parser.add_argument('-m', '--description', default='', type=str,
            help='description for slack notification')

    args = parser.parse_args()
    
    main(args)
