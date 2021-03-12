'''Oauth2 type authenticator.'''

import json
import my_env
# pylint: disable=E0401
import requests
import authenticator_header_bearer

def run(action):
    '''
    Run an action on an Oauth2 type provider.
    '''
    key = my_env.get('KEY')
    secret = my_env.get('SECRET')

    myvars = {
        'client_id': key,
        'client_secret': secret,
        'grant_type': 'client_credentials',
    }

    api_url = action.auth_base() + '/auth/oauth/token'

    response = requests.post(api_url, data=myvars)

    if response.status_code == 200:
        token = json.loads(response.content.decode('utf-8'))['access_token']
        return authenticator_header_bearer.run(action, token)
    print('==> COULD NOT GET A TOKEN')
    print(response.status_code)
    print(json.loads(response.content.decode('utf-8')))
    return None
