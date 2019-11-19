# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import Restarted, FollowupAction, SlotSet, UserUtteranceReverted

from helpers.microsoft_helper import MicrosoftAPI
from helpers.slack_halper import SlackAPI

import requests
import re
import json
import random
import string

def randomPassword(stringLength=10):
    """Generate a random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

def getSlackUser(sender_id):
    slack = SlackAPI()
    user = slack.get(
        route='/users.info',  
        params = {"user": sender_id}
    )
    if 'error' in user:
        return None
    else:
        return user

class DefaultFallback(Action):
    def name(self) -> Text:
        return "custom_fallback_action"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Don't understand what you mean! Please write again")
        return [UserUtteranceReverted()]

class ActionCreateUser(Action):

    def name(self) -> Text:
        return "action_create_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        MSApi = MicrosoftAPI(mod="default")
        
        user = getSlackUser(tracker.sender_id)
        if user == None:
            dispatcher.utter_message("Your email address cannot be used on the Azure portal. Only '@halykbank.kz' addresses are valid")
            return [Restarted()]

        email = user['user']['profile']['email']
        temp_password = randomPassword()
        
        if(re.search(r'@halykbank.kz', email)):

            userExist = MSApi.get(route="/users/"+email)
            if 'error' in userExist and userExist['error']['code'] == 'Request_ResourceNotFound':
                new_user_profile = {
                    "mailNickname": email.split('@')[0],
                    "userPrincipalName": email,
                    "displayName": user['user']['profile']['real_name'],
                    "accountEnabled": True,
                    "passwordProfile": {
                        "password": temp_password,
                        "forceChangePasswordNextSignIn": True
                    },
                }
                createResult = MSApi.post(route='/users', data=json.dumps(new_user_profile)).json()
                print(createResult)
                if 'error' in createResult:
                    dispatcher.utter_message("Something went wrong")
                    return [Restarted()]
                else:
                    responseString = "You have been successfully registrated! Your temporary password is "
                    responseString += temp_password
                    dispatcher.utter_message(responseString)
            else:
                dispatcher.utter_message("You are already registrated in Azure Portal")
                return [Restarted()]
        else:
            dispatcher.utter_message("You are not able to registrate in Azure portal")
            return [Restarted()]

        return []

class ActionInviteUser(Action):
    def name(self) -> Text:
        return "action_invite_user"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        MSApi = MicrosoftAPI(mod="uir")

        user = getSlackUser(tracker.sender_id)
        if user == None:
            dispatcher.utter_message("Your email address cannot be used on the Azure portal. Only '@halykbank.kz' addresses are valid")
            return [Restarted()]

        email = user['user']['profile']['email']

        inviteData = {
            "invitedUserDisplayName": user['user']['profile']['real_name'],
            "invitedUserEmailAddress": email,
            "inviteRedirectUrl": "https://portal.azure.com",
            "sendInvitationMessage": True,
            "invitedUser": {
                "userPrincipalName": email
            }
        }
        inviteResult = MSApi.post(route="/invitations", data=json.dumps(inviteData)).json()
        if 'error' in inviteResult:
            dispatcher.utter_message("The invention has not been sent... An error has occured")
            return []
        dispatcher.utter_message("You have been successfully invited to UIR directory. Please, confirm the invitation sent to your email.")
        return []

class ActionResetPassword(Action):
    def name(self) -> Text:
        return "action_reset_password"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user = getSlackUser(tracker.sender_id)
        if user is None:
            dispatcher.utter_message("Your email is invalid")
            return [Restarted()]
    
        email = user['user']['profile']['email']
        if(re.search(r'@halykbank.kz', email)):

            MSApi = MicrosoftAPI(mod="uir_user")

            temp_password = randomPassword()

            passwordProfile = {
                "passwordProfile": {
                    "password": temp_password,
                    "forceChangePasswordNextSignIn": True,
                }
            }
            resetResult = MSApi.patch(route="/users/"+email, data=json.dumps(passwordProfile))
            print(resetResult)
            if resetResult.status_code == 204:
                text = temp_password + " this is your temporary password"
                dispatcher.utter_message(text)
            else:
                dispatcher.utter_message("Something went wrong! Please, try latter")
                return [Restarted()]
        else:
            dispatcher.utter_message("Your email address cannot be used on the Azure portal. Only '@halykbank.kz' addresses are valid")
        return []