import json
import datetime
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class SlackNotificater:

    def divider_block(self):
        return { 'type': 'divider' }

    def markdown_block(self, text):
        block = {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn', 
                        'text': text
                    }
                }

        return block

    def multiple_field_block(self, fields):
        block = {
                    'type': 'section',
                    'fields': fields
                }

        return block

    def markdown_field(self, text):
        field = {
                    'type': 'mrkdwn',
                    'text': text
                }

        return field

    def send_slack_request(self, data):
        url = os.environ.get('SLACK_WEBHOOK_URL')
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        if response.status_code == requests.codes.ok:
            print('Response: ', response)
        else:
            print('Slack Notification Failed: ', response)

    def notificate(self, duration, args):

        data = {
            'blocks': [
                self.markdown_block(':tada: Topic Model Learning has finished :tada:\n' + args.description),
                self.divider_block(),
                self.markdown_block(':bulb: *Execution Information* :bulb:'),
                self.multiple_field_block([
                    self.markdown_field('*Input File*\n' + args.file_name),
                    self.markdown_field('*Output File*\n' + args.output_file),
                    self.markdown_field('*Duration*\n' + str(datetime.timedelta(seconds=duration)))
                ]),
                self.divider_block(),
                self.markdown_block(':gear: *Sample Configuration* :gear:'),
                self.multiple_field_block([
                    self.markdown_field('*Sample Iterations*\n' + str(args.num_samples)),
                    self.markdown_field('*Warmup Iterations*\n' + str(args.num_warmup)),
                    self.markdown_field('*Chain*\n' + str(args.num_chains)),
                    self.markdown_field('*Device*\n' + args.device)
                ])
            ]
        }

        self.send_slack_request(data)

    def notificate_svi(self, duration, args):

        data = {
            'blocks': [
                self.markdown_block(':fire: SVI Optimization has finished :fire:\n' + args.description),
                self.divider_block(),
                self.markdown_block(':bulb: *Execution Information* :bulb:'),
                self.multiple_field_block([
                    self.markdown_field('*Input File*\n' + args.file_name),
                    self.markdown_field('*Output File*\n' + args.output_file),
                    self.markdown_field('*Duration*\n' + str(datetime.timedelta(seconds=duration)))
                ]),
                self.divider_block(),
                self.markdown_block(':gear: *Optimization Configuration* :gear:'),
                self.multiple_field_block([
                    self.markdown_field('*Optimization Iterations*\n' + str(args.num_step)),
                    self.markdown_field('*Device*\n' + args.device)
                ])
            ]
        }

        self.send_slack_request(data)
