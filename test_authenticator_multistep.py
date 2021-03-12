'''
Test Authenticator Multistep.
See Testing Individual Files in README.md.
'''

import json
import authenticator_multistep
import my_env

print('')
print('try and set an environment variable to HELLO')
authenticator_multistep.assign({"jsonpath": "$.whatever", "var": "HELLO"},
                               json.dumps({"whatever" : "hello world"}))
print('fetching environment variable')
print(my_env.get('HELLO'))
