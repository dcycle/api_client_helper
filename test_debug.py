'''
Test Debug.
See Testing Individual Files in README.md.
'''

import os
import debug

debug.debug('location', 'this will not display')
os.environ['DEBUG'] = str(1)
debug.debug('location', 'this will display')
