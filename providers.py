'''
Get all providers.
'''

import os
import sys
PROVIDERS = sys.modules[__name__]

def all_providers():
    '''Get all providers.'''
    candidate = os.listdir(os.getcwd() + '/plugins')
    candidate.remove('README.md')
    return candidate

def comma_separated():
    '''Get all providers as a comma-separated string.'''
    return ', '.join(PROVIDERS.all_providers())
