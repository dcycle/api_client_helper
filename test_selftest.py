'''
Run self-tests.
See Testing Individual Files in README.md.
'''

import sys
import json
import os
import providers
import myyaml
SELFTEST = sys.modules[__name__]

def check_providers():
    '''
    checks loading providers.
    '''
    print("Checking providers")
    print("All providers")
    print(providers.all_providers())
    print("Comma-separated")
    print(providers.comma_separated())

def check_myyaml():
    '''
    checks for the My Yaml system.
    '''
    print("Checking my yaml")
    print(myyaml.load_action('digitalocean', 'accountinfo'))
    print(myyaml.load_provider('digitalocean'))
    print(myyaml.load_action('digitalocean', ''))
    print(myyaml.load('digitalocean'))
    print(myyaml.load('digitalocean', 'accountinfo'))

def check_misc():
    '''
    miscellaneous checks.
    '''
    print("Checking miscellaneous")
    print(json.dumps(True))

def run():
    '''Run self-tests.'''
    print("Running self-tests")
    print("Checking current working directory")
    print(os.getcwd())
    SELFTEST.check_myyaml()
    SELFTEST.check_providers()
    SELFTEST.check_misc()

SELFTEST.run()
