'''Interact with one provider, performing an action on it.'''

import yaml
import os
import sys
import deepmerge

myyaml = sys.modules[__name__]

def loadFile(file):
    with open(os.getcwd() + '/plugins/' + file + '.yml', 'r') as stream:
        return(yaml.safe_load(stream))

def loadProvider(provider):
    return myyaml.loadFile(provider + '/' + provider);

def loadAction(provider, action):
    if action == '':
        return {}
    return myyaml.loadFile(provider + '/' + action + '/' + action);

def load(provider, action = ''):
    ret = deepmerge.merge(myyaml.loadProvider(provider), myyaml.loadAction(provider, action))
    return ret
