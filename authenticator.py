'''Interact with one provider, performing an action on it.'''

def run(action):
    authenticator_name = action.data['authenticator']
    if (authenticator_name == 'header_bearer'):
        import authenticator_header_bearer
        return authenticator_header_bearer.run(action)
    elif (authenticator_name == 'oauth2'):
        import authenticator_oauth2
        return authenticator_oauth2.run(action)
    else:
        raise Exception('Unknown authenticator ' + authenticator_name)
