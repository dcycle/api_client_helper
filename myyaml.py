'''Interact with one provider, performing an action on it.'''

import os
import sys
# pylint: disable=E0401
import yaml
import deepmerge

MYYAML = sys.modules[__name__]

def load_file(file):
    '''
    Load a YAML file.
    '''
    with open(os.getcwd() + '/plugins/' + file + '.yml', 'r') as stream:
        return yaml.safe_load(stream)

def load_provider(provider):
    '''
    Load a provider's YAML file.
    '''
    return MYYAML.load_file(provider + '/' + provider)

def load_action(provider, action):
    '''
    Load an action file for a given provider.
    '''
    if action == '':
        return {}
    return MYYAML.load_file(provider + '/' + action + '/' + action)

def load(provider, action=''):
    '''
    Load YAML files for a provider and optionally its action, then
    merge them.
    '''
    ret = deepmerge.merge(MYYAML.load_provider(provider), MYYAML.load_action(provider, action))
    return ret
