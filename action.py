'''Interact with one provider, performing an action on it.'''

import myyaml
import authenticator
import my_env
import debug

class Action:
    '''
    Actions can be performed on providers, for example "account info" or
    "create widget" are actions.
    '''
    def __init__(self, data):
        '''
        Initialize the action.
        data: the action description from YML file(s).
        '''
        self.data = data
        if 'preflight' in data and 'env_variables' in data['preflight']:
            # pylint: disable=W0612
            for key, val in enumerate(data['preflight']['env_variables']):
                my_env.get(val['name'], val['desc'])
    def get_data(self, key, default):
        '''
        Get action description data from the YML files.
        key: description key such as "verb".
        default: return this if the key is absent.
        '''
        if key in self.data:
            return self.data[key]
        return default
    def run(self):
        '''
        Run the action.
        '''
        ret = authenticator.run(self)
        return ret
    def url(self):
        '''
        Get the action's URL.
        '''
        return self.data['base'] + self.path()
    def successcode(self):
        '''
        Get the action's expected success code.
        '''
        return self.get_data('successcode', 200)
    def expecting_content(self):
        '''
        Whether or not the action expects content.
        '''
        return self.get_data('expecting_content', 1)
    def path(self):
        '''
        Get the path of the action, for example /api/v2/whatever.
        '''
        candidate = self.data['path']
        # pylint: disable=W0612
        for key, val in enumerate(self.get_data('replace', {})):
            candidate = candidate.replace(val['string'], my_env.get(val['env_var']))
        return candidate
    def base(self):
        '''
        Get the base URL of the provider, for example https://example.com.
        '''
        return self.data['base']
    def auth_base(self):
        '''
        Get the authentication base URL of the provider, which can be
        different from the base URL.
        '''
        return self.data['auth_base']
    def verb(self):
        '''
        Get the action verb such as GET.
        '''
        return self.data['verb']
    def body(self):
        '''
        Get the body to pass to the API request.
        '''
        ret = {}
        # pylint: disable=W0612
        for key, val in enumerate(self.get_data('body', {})):
            ret[val['name']] = my_env.get(val['env_var'])
        debug.debug('action.body returning', ret)
        return ret

def from_provider_action(provider, action):
    '''
    Given provider and action strings, return an Action object..
    '''
    return Action(myyaml.load(provider, action))
