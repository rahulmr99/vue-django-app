import logging


class LexRuntimeResponse(object):
    """
    for sample response see, tests/data.py
    """

    def __init__(self, response: dict):
        self.dialogState: str = response.get('dialogState')
        self.intentName: str = response.get('intentName', '')
        self.sessionAttributes: dict = response.get('sessionAttributes') or {}
        self.slots: dict = response.get('slots') or {}
        self.message = response.get('message', '')

        logging.debug(f'Received Response from Lex: {self.message}')

    def __repr__(self):
        return f'<{type(self).__name__}>: {self.message}'

    @property
    def is_fulfilled(self):
        return self.dialogState in {'ReadyForFulfillment', 'Fulfilled', }


def validate_session_attributes(attrs: dict):
    return {key: str(val) for key, val in attrs.items()}
