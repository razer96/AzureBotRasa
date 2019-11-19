'''
    MicrosoftAPI class is an instance that requests graph.microsoft.com API

'''

import requests 
import os
class MicrosoftAPI:

    token = None
    apiURL = None

    def __init__(self, mod="default", user={}):

        self.apiURL = os.environ['MS_API']
        # self.apiURL = "https://graph.microsoft.com/v1.0"
        self.setToken(mod=mod, user=user)

    # Get application access toket
    def setToken(self, mod, user):

        options = {}
        if mod == 'default':
            options['url'] = "https://login.microsoftonline.com/"+os.environ['DEFAULT_DIR']+"/oauth2/v2.0/token"
            options['payload'] = {
                'client_id': os.environ['DEFAULT_CLIENT_ID'],
                'scope': 'https://graph.microsoft.com/.default',
                'client_secret': os.environ['DEFAULT_CLIENT_SECRET'],
                'grant_type': 'client_credentials'
            }
            
        elif mod == 'uir':
            options['url'] = "https://login.microsoftonline.com/"+os.environ['UIR_DIR']+"/oauth2/v2.0/token"
            options['payload'] =  {
                'client_id': os.environ['UIR_CLIENT_ID'],
                'scope': 'https://graph.microsoft.com/.default',
                'client_secret': os.environ['UIR_CLIENT_SECRET'],
                'grant_type': 'client_credentials'
            }

        elif mod == 'default_user':
            options['url'] = "https://login.microsoftonline.com/"+os.environ['DEFAULT_DIR']+"/oauth2/v2.0/token"
            options['payload'] = {
                'client_id': os.environ['DEFAULT_CLIENT_ID'],
                'scope': 'https://graph.microsoft.com/.default',
                'client_secret': os.environ['DEFAULT_CLIENT_SECRET'],
                'grant_type': 'password',
                'username': user['email'],
                'password': user['password']
            }
        elif mod == 'uir_user':
            options['url'] = "https://login.microsoftonline.com/"+os.environ['DEFAULT_DIR']+"/oauth2/v2.0/token"
            options['payload'] = {
                'client_id': os.environ['DEFAULT_CLIENT_ID'],
                'scope': 'https://graph.microsoft.com/.default',
                'client_secret': os.environ['DEFAULT_CLIENT_SECRET'],
                'grant_type': 'password',
                'username': os.environ['UIR_USERNAME'],
                'password': os.environ['UIR_PASSWORD']
            }
        response = requests.post(options['url'], data=options['payload'])

        if response.json()['access_token']:
            self.token = response.json()['access_token']

    # GET HTTP Method for graph API
    def get(self, route=None, params={}, data={}, headers={'Content-Type': 'application/json'}):

        if not route:
            return None

        headers['Authorization'] = 'Bearer ' + self.token
        response = requests.get(self.apiURL+route, headers=headers, params=params, data=data)
        return response.json()
    
    # POST HTTP Method for graph API
    def post(self, route=None, data={}, headers={'Content-Type': 'application/json'}):

        if not route:
            return None

        headers['Authorization'] = 'Bearer ' + self.token
        response = requests.post(self.apiURL+route, headers=headers, data=data)
        return response

    # PATCH HTTP Method for graph API
    def patch(self, route=None, data={}, headers={'Content-Type': 'application/json'}):

        if not route:
            return None

        headers['Authorization'] = 'Bearer ' + self.token
        response = requests.patch(self.apiURL+route, headers=headers, data=data)
        return response

