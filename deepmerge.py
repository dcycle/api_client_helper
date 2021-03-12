'''Deep merge.'''

import sys

DEEPMERGE = sys.modules[__name__]

# Adapted from https://stackoverflow.com/a/7205107/1207752
def merge(first, second, path=None):
    "merges second into first"
    if path is None:
        path = []
    for key in second:
        if key in first:
            if isinstance(first[key], dict) and isinstance(second[key], dict):
                DEEPMERGE.merge(first[key], second[key], path + [str(key)])
            elif isinstance(first[key], list) and isinstance(second[key], list):
                first[key] = first[key] + second[key]
            elif first[key] == second[key]:
                pass # same leaf value
            elif isinstance(first[key], str) and isinstance(second[key], str):
                first[key] = second[key]
            else:
                print(first[key])
                print(second[key])
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            first[key] = second[key]
    return first
