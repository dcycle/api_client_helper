'''A header-bearer type authenticator.'''

import json
# pylint: disable=E0401
import requests
import my_env

def run(action, token=None):
    '''
    Run an action on a header-bearer type provider.
    '''
    if token is None:
        token = my_env.get('TOKEN')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }

    api_url = action.url()
    body = action.body()
    verb = action.verb()

    if verb == 'get':
        response = requests.get(api_url, headers=headers, json=body)
    elif verb == 'post':
        response = requests.post(api_url, headers=headers, json=body)
    elif verb == 'delete':
        response = requests.delete(api_url, headers=headers, json=body)
    else:
        raise Exception('Unknow verb ' + verb)

    expectedcode = action.successcode()

    if response.status_code == expectedcode:
        if action.expecting_content():
            ret = response.content.decode('utf-8')
            return ret
        return json.dumps(True)
    print('ERROR - expected status code ' + str(expectedcode) + ' but got ')
    print(str(response.status_code))
    print(response.content.decode('utf-8'))
    return None
