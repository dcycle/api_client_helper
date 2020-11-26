'''Trying to get Acquia API to work.'''

import requests
import json
import os

key = os.getenv('KEY')
secret = os.getenv('SECRET')

myvars = {
    'client_id': key,
    'client_secret': secret,
    'grant_type': 'client_credentials',
}

url = 'https://accounts.acquia.com/api/auth/oauth/token'

response = requests.post(url, data=myvars)

if response.status_code == 200:
    token = json.loads(response.content.decode('utf-8'))['access_token']
    print('We managed to get an access token, it is ' + token)
    print('Trying to get account information using our token')
    headers = {
        'Authorization': 'Bearer ' + token
    }

    url = 'https://cloud.acquia.com/api/account'

    print('url')

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        print("Yes!")
        print(json.loads(response.content.decode('utf-8')))
    else:
        print("We got a token, but something went wrong when trying to get account info")
        print(json.loads(response.content.decode('utf-8')))
else:
    print('Something went wrong getting an access token')
    print(json.loads(response.content.decode('utf-8')))
