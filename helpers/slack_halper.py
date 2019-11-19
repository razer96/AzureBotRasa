'''
    SlackAPI class is an instance that requests slack.com/api 

'''
import os
import requests 

class SlackAPI:

    token = None
    apiURL = None

    def __init__(self):
        self.apiURL = "https://slack.com/api"
        self.token = os.environ['SLACK_TOKEN']

    def get(self, route=None, params={}, data={}, headers={'Content-Type': 'application/x-www-form-urlencoded'}):

        if not route:
            return None

        params['token'] = self.token
        response = requests.get(self.apiURL+route, headers=headers, params=params, data=data)
        return response.json()
        