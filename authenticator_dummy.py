'''A dummy authenticator.'''

import json

def run(my_action):
    '''
    Run an action on the dummy provider by return its mock response.
    Actions whose provider is "dummy" must define a response in their
    YML files. See for example ./plugins/dummy/dummy/dummy.yml.
    '''
    return json.dumps(my_action.get_data_with_replacements('response',None))
