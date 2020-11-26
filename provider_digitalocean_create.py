'''
Create a Digitalocean VM (droplet).
'''

import my_env
import json
import requests

def run():
    '''
    Intract with Digitalocean via its API
    '''
    token = my_env.get('TOKEN')
    api_url_base = 'https://api.digitalocean.com/v2/'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }

    api_url = '{0}droplets'.format(api_url_base)

    data = {}
    data['names'] = [
        my_env.get('NAME')
    ]
    data['region'] = my_env.get('REGION')
    data['size'] = my_env.get('SIZE')
    data['image'] = my_env.get('IMAGE')

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        print('HELLOs')
        print(json.loads(response.content.decode('utf-8')))
    else:
        print('WORLD')
        print(api_url_base)
        print(api_url)
        print(response.status_code)
        print(json.loads(response.content.decode('utf-8')))
        return None
