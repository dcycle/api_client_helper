'''Interact with one provider, performing an action on it.'''

import my_env
import requests
import json

def run(action):
    key = my_env.get('KEY')
    secret = my_env.get('SECRET')

    myvars = {
        'client_id': key,
        'client_secret': secret,
        'grant_type': 'client_credentials',
    }

    api_url = action.authBase() + '/auth/oauth/token'

    response = requests.post(api_url, data=myvars)

    if response.status_code == 200:
        token = json.loads(response.content.decode('utf-8'))['access_token']
        import authenticator_header_bearer
        return authenticator_header_bearer.run(action, token)
    else:
        print('==> COULD NOT GET A TOKEN')
        print(api_url_base)
        print(api_url)
        print(response.status_code)
        print(json.loads(response.content.decode('utf-8')))
        return None

    # data = {}
    # data['names'] = [
    #     my_env.get('NAME')
    # ]
    # data['region'] = my_env.get('REGION')
    # data['size'] = my_env.get('SIZE')
    # data['image'] = my_env.get('IMAGE')
    #
    # response = requests.post(api_url, json=data, headers=headers)
    #
