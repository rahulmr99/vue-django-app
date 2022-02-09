import pytest
from fnmatch import fnmatch


def assert_msg(message: str, resp: dict):
    assert message in resp['dialogAction']['message']['content']


class LexBotMock(object):
    def __init__(self, data: dict, handler: callable):
        self.event_data = data
        self.handler = handler

        self.last_response: dict = None

    def intend(self, intent_name):
        return self.call(intent_name=intent_name)

    @property
    def message(self):
        return self.last_response['dialogAction']['message']['content'] if self.last_response else None

    def __repr__(self):
        return f"<LexMock: {self.handler}> {self.message}"

    def call(
            self,
            intent_name: str = '',
            accept_intent=False,
            deny_intent=False,
            slots: dict = None
    ) -> 'LexBotMock':
        if intent_name:
            self.event_data['currentIntent']['name'] = intent_name
        # update confirmation status
        self.event_data['currentIntent']['confirmationStatus'] = (
            'Confirmed' if accept_intent
            else 'Denied' if deny_intent
            else 'None'
        )

        # update slots
        if slots:
            self.event_data['currentIntent']['slots'].update(slots)

        self.set_resp()

        return self

    def set_resp(self):
        resp = self.handler(self.event_data, {})
        self.event_data['sessionAttributes'] = resp['sessionAttributes']
        action = resp['dialogAction']
        if 'slots' in action:
            self.event_data['currentIntent']['slots'] = action['slots']
        self.last_response = resp

    def say(self, input: str = None, **slots):
        if input:
            self.event_data['inputTranscript'] = input
        return self.call(slots=slots)

    def say_yes(self):
        return self.call(accept_intent=True)

    def say_no(self):
        return self.call(deny_intent=True)

    def replied(self, pattern: str):
        """
            assert the replied message content
        Args:
            pattern: pattern compatible with fnmatch
        """
        __tracebackhide__ = True

        if pattern and '*' not in pattern:
            pattern = f'*{pattern}*'

        if not fnmatch(self.message, pattern):
            pytest.fail(f'Failed to match: {pattern}; Msg: {self.message}')
