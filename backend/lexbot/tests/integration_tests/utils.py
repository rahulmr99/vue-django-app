import os
from xml.etree import ElementTree


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    import django

    django.setup()


setup_django()

import copy
import requests
from django.urls import reverse

from lexbot.tests.views_test import get_sms_bot_url

from lexbot.tests.data import TEST_TWILIO_MSG_DATA

ph = '+919786834902'

# edit the below to match production/staging environment.
API_URL = "https://secure.bookedfusion.com"
LOGIN_URL = API_URL + reverse('login_token')

# You could get the JWT token from a browser session or can use the login API.
# COMPANY_ID = 22
# CRED_USER = "root@gmail.com"
# CRED_PWD = "BB290AA450CI"
COMPANY_ID = 15
CRED_USER = "michaellaurenzibuye@gmail.com"
CRED_PWD = "baller23$"

# no need to edit below
SMS_BOT_URL = API_URL + get_sms_bot_url(COMPANY_ID)


class LexBotInteractive(object):
    def __init__(self):
        self.token = None
        self.resp = None

        self._if_check_text = None

    def _post(self, url, data: dict = None):
        if not self.token:
            self._get_token()
        headers = {'Authorization': f"JWT {self.token}"}

        self.resp = requests.post(url, data=data, headers=headers)

    @property
    def reply(self):
        try:
            xml = ElementTree.fromstring(self.resp.content)
            return xml.getchildren()[0].text
        except Exception:
            return None

    def _get_token(self):
        self.resp = requests.post(LOGIN_URL, data={'email': CRED_USER, 'password': CRED_PWD})
        self.token = self.resp.json().get('token')
        if not self.token:
            raise Exception(f'Error getting JWT Token {self.resp.json()}')

    def _has_replied(self, text: str) -> bool:
        return (text is None) or (text in self.resp.content.decode()) or (text in self.reply)

    def say(self, text: str):
        if not self._has_replied(self._if_check_text):
            #  do not send the text to lexbot since the previous reply was different
            return self

        data = copy.deepcopy(TEST_TWILIO_MSG_DATA)
        data['Body'] = text
        self._post(SMS_BOT_URL, data)

        if self.resp.status_code in {404, 500}:
            print(f'Failed to get valid response. Code: {self.resp.status_code}')
            print(self.resp.content)
        return self

    def replied(self, text: str):
        if not self._has_replied(text):
            raise Exception(f'{text} is not Found in {self.resp.content.decode()}')

    def if_replied(self, text: str):
        self._if_check_text = text
        return self


LexBot = LexBotInteractive()
'''singleton to ease testing lex bot'''
