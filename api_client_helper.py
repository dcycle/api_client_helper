'''Interact with APIs as a client.'''

import argparse
import providers

parser = argparse.ArgumentParser(description='Interact with APIs as a client.')
parser.add_argument('provider', metavar='provider', type=str,
                   help='A provider to interact with; available providers are ' + providers.comma_separated() + '.')
parser.add_argument('action', metavar='action', type=str,
                   help='An action to run; use "help" if not sure.')
parser.add_argument('--selftest', default=0,
                   help='Use 1 to ignore other arguments and self-test the code (default: 0)')
parser.add_argument('--jsonpath', default="$",
                   help='Jsonpath (default = $)')
parser.add_argument('--debug', default=0,
                   help='Use 1 to print debug information (default: 0)')

args = parser.parse_args()

if getattr(args, 'selftest'):
    import selftest
    selftest.run()
else:
    import action
    action_object = action.from_provider_action(args.provider, args.action).run()
    print(26)
    print('just got ' + action_object)
    from jsonpath_ng import jsonpath, parse
    import json
    print('zzz')
    print([match.value for match in parse(getattr(args, 'jsonpath')).find(action_object)])
    print('zzz')

# provider.get(PARSER).run(PARSER.parse_args().action)
