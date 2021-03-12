'''
Test My Jsonpath.
See Testing Individual Files in README.md.
'''

import my_jsonpath

SAMPLE = '''
{"account": {"droplet_limit": 25,"floating_ip_limit": 3,"volume_limit": 100, "email": "admin@example.com","uuid": "abc123", "email_verified": true, "status": "active","status_message": ""}}
'''
SAMPLE2 = '''
{"ip": [{"ip_address": "10.132.0.9", "netmask": "255.255.0.0", "gateway": "", "type": "private"}, {"ip_address": "167.71.249.143", "netmask": "255.255.240.0", "gateway": "167.71.240.1", "type": "public"}]}
'''
SAMPLE3 = '''
[{"ip_address": "10.132.0.9", "netmask": "255.255.0.0", "gateway": "", "type": "private"}, {"ip_address": "167.71.249.143", "netmask": "255.255.240.0", "gateway": "167.71.240.1", "type": "public"}]
'''

print('')
print('my_jsonpath')
print('-----')
print('Fetch parts of a Json.')
print('See also https://www.journaldev.com/33265/python-jsonpath-examples.')
print('')
print('Our json is')
print('-----')
print(SAMPLE)
print('')
print('Returning the original json')
print('-----')
print('my_jsonpath.find(SAMPLE), my_jsonpath.find(SAMPLE, None), and')
print('my_jsonpath.find(SAMPLE, None, None) will return the SAMPLE:')
print('')
print(my_jsonpath.find(SAMPLE))
print(my_jsonpath.find(SAMPLE, None))
print(my_jsonpath.find(SAMPLE, None, None))
print('')
print('Returning part of the original json')
print('-----')
print('')
print('my_jsonpath.find(SAMPLE, "$.account")')
print('')
print(my_jsonpath.find(SAMPLE, '$.account'))
print('')
print('my_jsonpath.find(SAMPLE, "$.account.volume_limit")')
print('')
print(my_jsonpath.find(SAMPLE, '$.account.volume_limit'))
print('')
print(my_jsonpath.find(SAMPLE2, '$.ip'))
print('')
print(my_jsonpath.find(SAMPLE2, '$.ip[?(@.type = "public")].ip_address'))
print('')
print(my_jsonpath.find(SAMPLE3, '$[?(@.type = "public")].ip_address'))
print('')
print('Use a default if no match')
print('-----')
print('')
print('my_jsonpath.find(SAMPLE, "$.does-not-exist")')
print(my_jsonpath.find(SAMPLE, '$.does-not-exist'))
print('')
print('my_jsonpath.find(SAMPLE, "$.does-not-exist", "Hi there")')
print(my_jsonpath.find(SAMPLE, '$.does-not-exist', 'Hi there'))
