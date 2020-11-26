'''Interact with one provider, performing an action on it.'''

import my_env
import requests
import json

def run(action, token = None):
    if (token == None):
        token = my_env.get('TOKEN')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }

    api_url = action.url()
    body = action.body()
    verb = action.verb()

    if (verb == 'get'):
        response = requests.get(api_url, headers=headers, json=body)
    elif (verb == 'post'):
        response = requests.post(api_url, headers=headers, json=body)
    elif (verb == 'delete'):
        response = requests.delete(api_url, headers=headers, json=body)
    else:
        raise Exception('Unknow verb ' + verb)

    expectedcode = action.successcode()

    if response.status_code == expectedcode:
        if (action.expectingContent()):
            ret = response.content.decode('utf-8')
            print('returning ' + ret)
            print(34)
            return ret
        else:
            print('Success')
            return json.encode(true)
    else:
        print('ERROR - expected status code ' + str(expectedcode) + ' but got ' + str(response.status_code))
        print(json.loads(response.content.decode('utf-8')))
        return None
