import argparse
import csv
import os
from os.path import join, dirname
import time
from dotenv import load_dotenv
from collections import defaultdict

import boto3
import comet_ml
import pyro
import pyro.distributions as dist
import torch
from botocore.exceptions import ClientError
from comet_ml import api
from tqdm import tqdm

device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def download_posterior(exp_key):
    session = boto3.Session(profile_name=os.environ.get('AWS_PROFILE'))
    s3 = session.client('s3')

    bucket_name = os.environ.get('AWS_BUCKET')
    file_name = exp_key + '.pkl'
    try:
        s3.download_file(bucket_name, file_name, file_name)
    except ClientError as e:
        print(e)
        raise

def get_test_data(data_file, test_ids):
    with open(data_file) as f:
        reader = csv.reader(f)
        
        us = []
        ts = []
        ls = []
        tag_matrix = []

        for i, row in enumerate(reader):
            if i in test_ids:
                us.append(int(row[1]))
                ts.append(int(row[2]))
                ls.append(int(row[3]))
                tag_matrix.append([int(t) for t in row[4].split(",")])

    data = {
        'u': torch.LongTensor(us).to(device),
        't': torch.LongTensor(ts).to(device),
        'l': torch.LongTensor(ls).to(device),
        'tag': torch.LongTensor(tag_matrix).to(device)
    }

    return data

def divide_data_by_user(data, posterior):
    user_count = posterior['gamma_q'].shape[1]
    location_count= posterior['beta_q'].shape[1]

    user_location_matrix = torch.zeros(user_count, location_count).to(device)

    for u, l in zip(data['u'], data['l']):
        user_location_matrix[u][l] += 1

    return user_location_matrix

def create_location_ranking(posterior, sample_size):
    alpha_q = posterior['alpha_q'].to(device)
    gamma_q = posterior['gamma_q'].to(device)
    beta_q = posterior['beta_q'].to(device)

    size = torch.LongTensor([sample_size]).to(device)
    
    theta = dist.Dirichlet(alpha_q).sample(size)
    pi = dist.Dirichlet(gamma_q).sample(size)
    phi = dist.Dirichlet(beta_q).sample(size)

    probs = (theta.view(size, -1, 1, 1) * pi.unsqueeze(3) * phi.unsqueeze(2)).sum(1)
    ranking = torch.argsort(probs, dim=2, descending=True)
    # ranking: (sample_size, user_count, location_count)

    return ranking

def evaluate_location_precision_and_recall(ranking, k, data):
    # ranking: (sample_size, user_count, location_count)
    # data: (user_count, location_count)

    ranking_top_k = ranking[:,:,:k]

    ranking_top_k_bag = torch.zeros(ranking.shape).to(device).scatter_(2, ranking_top_k, 1)

    top_k_correct_bag = torch.logical_and(ranking_top_k_bag, data.expand(ranking_top_k_bag.shape))
    # top_k_correct_bag: (sample_size, user_count, location_count) 
    top_k_correct_count_per_user = torch.mean(top_k_correct_bag.type(torch.Tensor).sum(2), 0).to(device)
    # top_k_correct_count_per_user: (user_count)

    user_count_having_locations = torch.sum(data.sum(1) != 0).to(device)

    precision = torch.sum(top_k_correct_count_per_user) / user_count_having_locations / k

    recalls = top_k_correct_count_per_user / data.sum(1)
    recalls[torch.isnan(recalls)] = 0
    recalls[recalls == float('inf')] = 0
    recall = torch.sum(recalls) / user_count_having_locations

    return {f"location_precision@{k}": precision.to('cpu').item(), f"location_recall@{k}": recall.to('cpu').item()}

def calc_score(posterior, model_type, data):
    if model_type not in ['base', 'time', 'location', 'union', 'timeaware']:
        return

    result_metrics = {}
    sample_size = 10

    ranking = create_location_ranking(posterior, sample_size)

    pre_recall_at_one = evaluate_location_precision_and_recall(ranking, 1, data)
    result_metrics.update(pre_recall_at_one)
    print(pre_recall_at_one)

    pre_recall_at_five = evaluate_location_precision_and_recall(ranking, 5, data)
    result_metrics.update(pre_recall_at_five)
    print(pre_recall_at_five)

    pre_recall_at_ten = evaluate_location_precision_and_recall(ranking, 10, data)
    result_metrics.update(pre_recall_at_ten)
    print(pre_recall_at_ten)

    return result_metrics

def run(ex):
    eid = ex.id
    # filter
    if not ex.get_metrics(metric="duration"):
        # not yet finished
        print('Not finished: {} \n'.format(eid))
        return

    try:
        print('start: ', eid)

        # download posterior
        download_posterior(eid)

        posterior = torch.load(eid + '.pkl')

        # prepare test data
        test_data = get_test_data(posterior['data_file'], posterior['test_ids'])
        data_per_user = divide_data_by_user(test_data, posterior)

        # evaluation
        metrics = calc_score(posterior, ex.get_tags()[0], data_per_user)

        # log update
        ex.log_metrics(metrics)

        # rm pickl
        if os.path.exists(eid + '.pkl'):
            os.remove(eid + '.pkl')
        else:
            print('Could not remove: ', eid + '.pkl')

        print('done: ', eid, "\n")
    except ClientError:
        print('error: ', eid, "\n")
        return

def main(args):
    print(args)
    api_key = os.environ.get('COMET_API_KEY')
    workspace_name = os.environ.get('COMET_WORKSPACE')
    if args.debug:
        project_name = 'test'
    else:
        project_name = os.environ.get('COMET_PROJECT')

    # get experiments
    api_instance = api.API(api_key=api_key)
    q = ((api.Metric('duration') != None) & (api.Parameter('group_count') <= 15))
    exs = api_instance.query(workspace_name, project_name, q)

    for ex in exs:
        run(ex)

if __name__ == '__main__':
    assert pyro.__version__.startswith('1.3.1')
    pyro.enable_validation()
    parser = argparse.ArgumentParser(description='pyro model evaluation')
    parser.add_argument('--debug', action='store_true', help='debug mode')

    args = parser.parse_args()
    
    main(args)
