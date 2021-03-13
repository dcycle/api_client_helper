'''Interact with APIs as a client.'''

import sys
import argparse
import providers

PARSER = argparse.ArgumentParser(description='Interact with APIs as a client.')
PARSER.add_argument('provider', metavar='provider', type=str,
                    help='A provider to interact with; available providers' +
                    'are ' + providers.comma_separated() + '.')
PARSER.add_argument('action', metavar='action', type=str,
                    help='An action to run; use "help" if not sure.')
PARSER.add_argument('--selftest', default=0,
                    help='Use 1 to ignore other arguments and self-test the' +
                    'code (default: 0)')
PARSER.add_argument('--jsonpath', default="$", help='Jsonpath (default = $)')
PARSER.add_argument('--jsondecodefirst', default=0,
                    help='Use 1 to print the decoded version of the json' + 'string')
PARSER.add_argument('--debug', default=0,
                    help='Use 1 to print debug information (default: 0)')

ARGS = PARSER.parse_args()

if getattr(ARGS, 'selftest'):
    # pylint: disable=E0401
    import selftest
    selftest.run()
else:
    import action
    JSON_STRING = action.from_provider_action(ARGS.provider, ARGS.action).run()
    if JSON_STRING is None:
        print('Could not complete the request. Please run with --DEBUG=1 for details.')
        sys.exit(1)
    import json
    import my_jsonpath
    CANDIDATE = my_jsonpath.find(JSON_STRING, getattr(ARGS, 'jsonpath'))
    if getattr(ARGS, 'jsondecodefirst'):
        print(json.loads(CANDIDATE)[0])
    else:
        print(CANDIDATE)
