'''Run self-tests.'''

import sys
import os
selftest = sys.modules[__name__]

def checkProviders():
    print ("Checking providers")
    import providers
    print ("All providers")
    print (providers.all())
    print ("Comma-separated")
    print (providers.comma_separated())

def checkProvider():
    print ("Checking provider")
    import provider
    print ("Current providers")
    print (provider.from_arg('digitalocean'))

def checkMyyaml():
    print ("Checking my yaml")
    import myyaml
    print (myyaml.loadAction('digitalocean', 'smoke'))
    print (myyaml.loadProvider('digitalocean'))
    print (myyaml.loadAction('digitalocean', ''))
    print (myyaml.load('digitalocean'))
    print (myyaml.load('digitalocean', 'smoke'))

def run():
    '''Run self-tests.'''
    print ("Running self-tests")
    print ("Checking current working directory")
    print (os.getcwd())
    selftest.checkMyyaml()
    selftest.checkProviders()
    selftest.checkProvider()
