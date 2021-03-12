'''Allows running an action on its authenticator.'''

import authenticator_header_bearer
import authenticator_oauth2
import authenticator_dummy
import authenticator_multistep

def run(action):
    '''
    Run an action on its authenticator.
    '''
    authenticator_name = action.data['authenticator']
    if authenticator_name == 'multistep':
        return authenticator_multistep.run(action)
    if authenticator_name == 'header_bearer':
        return authenticator_header_bearer.run(action)
    if authenticator_name == 'oauth2':
        return authenticator_oauth2.run(action)
    if authenticator_name == 'dummy':
        return authenticator_dummy.run(action)
    raise Exception('Unknown authenticator ' + authenticator_name)
