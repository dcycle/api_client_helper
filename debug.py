'''Get environment variables and raise exception if they are not defined.'''

import inspect
import my_env

def debug(location, message):
    '''Debug a message if DEBUG env variable is true'''
    caller = inspect.stack()[1]
    caller_info = caller.filename + ':' + str(caller.lineno)
    if my_env.get_or_default('DEBUG', 0):
        print("[DEBUG " + caller_info + "] " + str(location) + ": " + str(message))
