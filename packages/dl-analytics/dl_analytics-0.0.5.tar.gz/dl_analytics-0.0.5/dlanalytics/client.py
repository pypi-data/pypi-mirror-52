import requests
import urllib
import json
from datetime import datetime
from .utils import dict2obj, NpEncoder
from .telegram import TelegramStats
PROJECT_ROOT = '/project'

class Analytics():

    def __init__(self, host='127.0.0.1', port=80, telegram_secret_key=None, telegram_group_key=None):
        '''
            host: static ip to your server
            telegram_secret_key: secret key to access your telegram bot
            telegram group_key : group id key
        '''
        self.telebot = None
        if telegram_secret_key and telegram_group_key:
            self.telebot = TelegramStats(secret_key=telegram_secret_key, group_key=telegram_group_key)
        
        if port  != 80:
            self.target_url = 'http://' + host + ':' + str(port)
        else:
            self.target_url = 'http://' + host
        res = requests.get(self.target_url+'/ping')
        self.latest_project_id = None
        if res.status_code != requests.codes.ok:
            raise ValueError('Unable to reach server')

    def check_connection(self):
        res = requests.get(self.target_url+'/ping')
        self.latest_project_id = None
        if res.status_code != requests.codes.ok:
            return False
        return True
    
    def create_project(self, name, description, search_space=None):
        res = requests.get(self.target_url+'/project/'+str(name))
        if res.status_code != requests.codes.ok:
            data = {
                'name': name,
                'description': description,
            }
            if search_space is not None and isinstance(search_space, dict):
                data['search_space'] = search_space
            
            res = requests.post(self.target_url+'/project', data=json.dumps(data, cls=NpEncoder), headers={
                'Content-Type': 'application/json'
            })
            if res.status_code != requests.codes.ok:
                raise ValueError('Unable to create project : %s' % res.text)
            project = res.json()
            self.latest_project_id = project['id']
            return project, True
        self.latest_project_id = res.json()['id']
        return dict2obj(res.json()), False

    def project(self, project_id=None):
        if project_id is None:
            if self.latest_project_id is None:
                raise ValueError('Project ID should be provided')
            project_id = self.latest_project_id
        url  = '{}/project/{}'.format(self.target_url, project_id)
        res = requests.get(url)
        if res.status_code != requests.codes.ok:
            raise ValueError('Unable to retrieve project : %s '% res.text)
        trial = res.json()
        return dict2obj(trial)

    def list_project(self):
        res = requests.get(self.target_url+'/project')
        if res.status_code != requests.codes.ok:
            raise ValueError('Unable to list project: Network error')
        raw_projects = res.json()
        if raw_projects['count'] > 0:
            return [ dict2obj(p) for p in raw_projects['projects'] ]
        return []

    def get_hyperopt_params(self, project_name):
        url  = '{}/project/{}/hyperopt'.format(self.target_url , project_name)
        res = requests.get(url)
        if res.status_code != requests.codes.ok:
            return None
        trial = res.json()
        if trial['is_assigned'] and 'status' not in trial:
            return dict2obj(trial)
        else:
            return None

    def update_hyperopt_results(self, project_name, trial_id, results):
        '''results

        '''
        if 'total_acc' not in results:
            raise ValueError('Must have total_acc attribute')

        payload = results
        if len(payload) == 0:
            return None

        url  = '{}/project/{}/hyperopt/{}'.format(self.target_url , project_name , trial_id)
        res = requests.post(url, data=json.dumps(payload, cls=NpEncoder), headers={
            'Content-Type': 'application/json'
        })

        if res.status_code != requests.codes.ok:
            return None

        trial = res.json()
        if self.telebot is not None:
            self.telebot.send_msg('Trial {} updated'.format(trial['updated']['name']))
        if 'status' not in trial:
            return dict2obj(trial)
        else:
            return None

    def create_trial(self, name, params, description=None, project_id=None, n_fold=None, results=None, machine='default', data_metadata=None  ):
        if project_id is None:
            if self.latest_project_id is None:
                raise ValueError('Project ID should be provided')
            project_id = self.latest_project_id

        payload = {
            'name': name,
            'params': params,
        }
        if description:
            payload['description'] = description
        if n_fold is not None:
            payload['n_fold'] = n_fold
        if results:
            payload['results'] = results
        if machine:
            payload['machine'] = machine
        if data_metadata:
            payload['data_metadata'] = data_metadata

        url  = '{}/project/{}/trial'.format(self.target_url, project_id)
        res = requests.post(url, data=json.dumps(payload, cls=NpEncoder), headers={
            'Content-Type': 'application/json'
        })
        if res.status_code != requests.codes.ok:
            raise ValueError('Unable to create a new trial %s' % res.text)
        trial = res.json()
        if self.telebot is not None:
            self.telebot.send_msg('Trial {} created, this is the {} nth fold'.format(trial['name'], trial['n_fold']))
        return dict2obj(trial)
    
    def from_args(self, name, args, description=None, project_id=None, machine=None, n_fold=None, data_metadata=None):
        if description is None:
            description = 'Trial run at {}'.format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        params = vars(args)
        return self.create_trial(name, params, description=description, project_id=project_id, n_fold=n_fold, data_metadata=data_metadata )

    def update_trial(self, trial_id, params=None,project_id=None, n_fold=None, results=None, data_metadata=None):
        '''
            return : return updated instance if trial_id is found, else return a None type
        '''
        if project_id is None:
            if self.latest_project_id is None:
                raise ValueError('Project ID should be provided')
            project_id = self.latest_project_id
        payload = {}
        if params is not None:
            payload['params'] = params
        if n_fold is not None:
            payload['n_fold'] = n_fold
        if results is not None:
            payload['results'] = results
        if data_metadata is not None:
            payload['data_metadata'] = data_metadata
        if len(payload) == 0:
            return None

        url  = '{}/project/{}/trial/{}'.format(self.target_url , project_id , trial_id)
        res = requests.post(url, data=json.dumps(payload, cls=NpEncoder), headers={
            'Content-Type': 'application/json'
        })

        if res.status_code != requests.codes.ok:
            raise ValueError('Unable to update trial %s' % res.text)
        trial = res.json()
        if self.telebot is not None:
            self.telebot.send_msg('Trial {} updated'.format(trial['updated']['name']))
        if trial['update'] > 0:
            return dict2obj(trial['updated'])
        else:
            return None