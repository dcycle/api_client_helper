'''Get all providers.'''

import os
import sys
providers = sys.modules[__name__]

def all():
    '''Get all providers.'''
    candidate = os.listdir(os.getcwd() + '/plugins')
    candidate.remove('README.md')
    return candidate

def comma_separated():
    '''Get all providers as a comma-separated string.'''
    return ', '.join(providers.all())
