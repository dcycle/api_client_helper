'''Get environment variables and raise exception if they are not defined.'''

import my_env;

def debug(location, message):
    '''Debug a message if DEBUG env variable is true'''
    if my_env.getOrDefault('DEBUG', 0):
        print ("[DEBUG] " + str(location))
        print ("[DEBUG] " + str(message))
