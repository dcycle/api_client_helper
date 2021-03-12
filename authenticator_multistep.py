'''A multistep authenticator.'''

import json
import action
import debug
import os
import sys
import time
import my_env
import my_jsonpath

AUTHENTICATOR_MULTISTEP = sys.modules[__name__]

def assign(val, json_string):
    '''
    Set an environment variable if possible.
    val: dict having possible key assign, which itself has key jsonpath,
      for example $.whatever, and var, for example: ID
    json: a json string
    '''
    CANDIDATES = my_jsonpath.find(val, '$.assign', [])
    # pylint: disable=W0612
    debug.debug('assignment', CANDIDATES);
    for key, candidate in enumerate(json.loads(CANDIDATES)):
        ENV_VAR = candidate['var']
        VALUE = my_jsonpath.find(json_string, candidate['jsonpath'])
        debug.debug('assignment', 'Assigning environment variable ' +
            ENV_VAR + ' to ' + VALUE);
        os.environ[ENV_VAR] = VALUE

def run(my_action):
    '''
    Runs several steps on a multistep process.
    '''
    last = None
    for key, val in enumerate(my_action.data['steps']):
        success = False
        MY_ACTION = action.from_provider_action(val['provider'], val['action'])
        debug.debug('message', '===> STEP ' + str(key));
        for try_number in range(val['max_wait']):
            debug.debug('message', 'Try ' + str(try_number) + ' of ' + str(val['max_wait']));
            JSON_STRING = MY_ACTION.run()
            debug.debug('message', JSON_STRING);
            last = JSON_STRING
            CANDIDATE = my_jsonpath.find(JSON_STRING, val['jsonpath'])
            if CANDIDATE == val['expected']:
                debug.debug('multistep', 'Success, moving to next step');
                AUTHENTICATOR_MULTISTEP.assign(json.dumps(val), JSON_STRING)
                success = True
                break;
            debug.debug('multistep', 'We do not yet have the required output.');
            debug.debug('multistep', CANDIDATE + ' != ' + val['expected']);
            debug.debug('multistep', 'Keep going.');
            time.sleep(1)
    if success:
        debug.debug('multistep', 'Multistep action succeeded')
        return last
    debug.debug('multistep', 'ERROR our multiple action')
    return None
