'''Get environment variables and raise exception if they are not defined.'''
import os

def get(var, desc=""):
    '''Get an environment variable, raise exception if it is not defined'''
    candidate = os.getenv(var)
    if candidate is None:
        raise Exception(f"""{desc}. Please set the {var} environment variable
        before calling the script: export {var}=whatever""")
    return candidate

def get_or_default(var, default):
    '''Get an environment variable, raise exception if it is not defined'''
    candidate = os.getenv(var)
    if candidate is None:
        return default
    return candidate
