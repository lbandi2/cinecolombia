import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def get_secret(secret_key, lst='no_list'):
    with open(f'{DIR_PATH}/.secrets') as f:
        lines = f.read().splitlines()
        for x in lines:
            if secret_key in x:
                if lst == 'list':
                    secret = list(x.split(' = ')[1].split(', '))
                    return secret
                else:
                    return x.split(' = ')[1]
