'''A multistep authenticator.'''

import os
import sys
import time
import json
import action
import debug
import my_jsonpath

AUTHENTICATOR_MULTISTEP = sys.modules[__name__]

def assign(val, json_string):
    '''
    Set an environment variable if possible.
    val: dict having possible key assign, which itself has key jsonpath,
      for example $.whatever, and var, for example: ID
    json: a json string
    '''
    candidates = my_jsonpath.find(val, '$.assign', [])
    # pylint: disable=W0612
    debug.debug('assignment', candidates)
    for key, candidate in enumerate(json.loads(candidates)):
        env_var = candidate['var']
        value = my_jsonpath.find(json_string, candidate['jsonpath'])
        debug.debug('assignment', 'Assigning environment variable ' +
                    env_var + ' to ' + value)
        os.environ[env_var] = value

def run(my_action):
    '''
    Runs several steps on a multistep process.
    '''
    last = None
    for key, val in enumerate(my_action.data['steps']):
        success = False
        step_action = action.from_provider_action(val['provider'], val['action'])
        debug.debug('message', '===> STEP ' + str(key))
        for try_number in range(val['max_wait']):
            debug.debug('message', 'Try ' + str(try_number) + ' of ' + str(val['max_wait']))
            json_string = step_action.run()
            debug.debug('message', json_string)
            last = json_string
            candidate = my_jsonpath.find(json_string, val['jsonpath'])
            if candidate == val['expected']:
                debug.debug('multistep', 'Success, moving to next step')
                AUTHENTICATOR_MULTISTEP.assign(json.dumps(val), json_string)
                success = True
                break
            debug.debug('multistep', 'We do not yet have the required output.')
            debug.debug('multistep', candidate + ' != ' + val['expected'])
            debug.debug('multistep', 'Keep going.')
            time.sleep(1)
    if success:
        debug.debug('multistep', 'Multistep action succeeded')
        return last
    debug.debug('multistep', 'ERROR our multiple action')
    return None
