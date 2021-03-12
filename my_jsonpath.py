'''
My Jsonpath.
Find parts of Json strings.
See Testing Individual Files in README.md.
'''

import sys
import json
# See https://github.com/h2non/jsonpath-ng/issues/8#issuecomment-349408047
# pylint: disable=E0401
from jsonpath_ng.ext import parse

MY_JSONPATH = sys.modules[__name__]

def find(json_string, query=None, default=None):
    '''
    Find part of a Json string.
    json_string: a json string such as {"account": {"droplet_limit": 25,
    "floating_ip_limit": 3, "volume_limit": 100, "email": "admin@example.com",
    "uuid": "abc123", "email_verified": true, "status": "active",
    "status_message": ""}}
    query: a query such as None (which will return the original string).
    default: a default value if the query string yields an empty result. The
    default value will be jsonized.
    '''

    if not query:
        return json_string

    json_data = json.loads(json_string)

    jsonpath_expression = parse(query)

    match = jsonpath_expression.find(json_data)

    ret = []
    for counter in range(len(match)):
        ret.append(match[counter].value)

    if ret == []:
        return json.dumps(default)
    return json.dumps(ret)
