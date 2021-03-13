'''A multistep authenticator.'''

import os
import sys
import time
import json
import action
import debug
import my_env
import my_jsonpath

AUTHENTICATOR_MULTISTEP = sys.modules[__name__]

def assign(val, json_string):
    '''
    Set an environment variable if possible.
    val: json of dict having possible key assign, which itself has an array,
      each item having key jsonpath,
      for example $.whatever, and var, for example: ID
    json: a json string
    '''
    candidates = my_jsonpath.find(val, '$.assign', [], True)
    # pylint: disable=W0612
    for key, candidate in enumerate(json.loads(candidates)):
        env_var = candidate['var']

        jsonpath = candidate['jsonpath']
        debug.debug('assignment', 'Checking if jsonpath needs replacements')
        if 'replace' in candidate:
            debug.debug('assignment', 'replace key exists')
            # pylint: disable=W0612
            for key2, val2 in enumerate(candidate['replace']):
                debug.debug('assignment', 'about to perform replacement')
                jsonpath = jsonpath.replace(val2['string'], my_env.get(val2['env_var']))

        debug.debug('assignment', jsonpath)
        value = my_jsonpath.find(json_string, jsonpath, None, True)
        debug.debug('assignment', 'Assigning environment variable ' +
                    env_var + ' to ' + value)
        os.environ[env_var] = value

def max_wait(step):
    '''
    get the max wait time in seconds for this step. Will be 1 or above.
    step: a step dict.
    '''
    if 'max_wait' in step and step['max_wait'] >= 1:
        return step['max_wait']
    return 1

def run(my_action):
    '''
    Runs several steps on a multistep process.
    '''
    last = None
    for key, val in enumerate(my_action.data['steps']):
        success = False
        step_action = action.from_provider_action(val['provider'], val['action'])
        debug.debug('message', '===> STEP ' + str(key))
        my_max_wait = AUTHENTICATOR_MULTISTEP.max_wait(val)
        for try_number in range(my_max_wait):
            debug.debug('message', 'Try ' + str(try_number) + ' of ' + str(my_max_wait))
            json_string = step_action.run()
            debug.debug('message', json_string)
            last = json_string
            candidate = my_jsonpath.find(json_string, val['jsonpath'] if 'jsonpath' in val else '$')
            if 'expected' not in val or candidate == json.dumps(val['expected']):
                debug.debug('multistep', 'Success, moving to next step')
                AUTHENTICATOR_MULTISTEP.assign(json.dumps(val), json_string)
                success = True
                break
            debug.debug('multistep', 'We do not yet have the required output.')
            debug.debug('multistep', candidate + ' != ' + json.dumps(val['expected']))
            debug.debug('multistep', 'Keep going.')
            time.sleep(1)
    if success:
        debug.debug('multistep', 'Multistep action succeeded')
        return last
    debug.debug('multistep', 'ERROR: our multiple action did not complete' +
                ' successfully. Run with DEBUG=1 for details.')
    return None
