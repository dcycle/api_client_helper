'''Intract with Digitalocean via its API.'''

def run(action):
    '''Intract with Digitalocean via its API'''
    if action == 'create':
        import create as action
    else:
        raise Exception('Unknown action ' + action)

    action.run()
