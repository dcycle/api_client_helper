'''Deep merge.'''

import sys

deepmerge = sys.modules[__name__]

# Adapted from https://stackoverflow.com/a/7205107/1207752
def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deepmerge.merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                a[key] = a[key] + b[key]
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                print(a[key])
                print(b[key])
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
