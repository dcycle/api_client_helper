'''Interact with one provider, performing an action on it.'''

import myyaml
import os
import authenticator
import my_env
import debug

class Action:
    def __init__(self, data):
        self.data = data
        for idx, val in enumerate(data['preflight']['env_variables']):
            my_env.get(val['name'], val['desc'])
    def getData(self, key, default):
        if key in self.data:
            return self.data[key]
        return default
    def run(self):
        return authenticator.run(self)
    def url(self):
        return self.data['base'] + self.path()
    def successcode(self):
        return self.getData('successcode', 200)
    def expectingContent(self):
        return self.getData('expectingContent', 1)
    def path(self):
        candidate = self.data['path']
        for idx, val in enumerate(self.getData('replace', {})):
            candidate = candidate.replace(val['string'], my_env.get(val['env_var']))
        return candidate
    def base(self):
        return self.data['base']
    def authBase(self):
        return self.data['auth_base']
    def verb(self):
        return self.data['verb']
    def body(self):
        ret = {}
        for idx, val in enumerate(self.getData('body', {})):
            ret[val['name']] = my_env.get(val['env_var'])
        debug.debug('action.body returning', ret)
        return ret;

def from_provider_action(provider, action):
    return Action(myyaml.load(provider, action))
