""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """
from typing import Union


def build_response(session_attributes: dict, dialogaction_type: str, **kwargs) -> dict:
    """build dict that can be passed to lex as response from lambda function handler"""
    resp = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': dialogaction_type,
        }
    }

    for key, val in kwargs.items():
        if val is not None:
            resp['dialogAction'][key] = val
    return resp


def elicit_slot(session_attributes: dict, intent_name: str, slots: dict, slot_to_elicit: str,
                message: Union[str, dict],
                response_card: dict = None):
    if type(message) == str:
        message = msg_text_content(message)

    return build_response(
        session_attributes, 'ElicitSlot',
        slots=slots,
        intentName=intent_name,
        slotToElicit=slot_to_elicit,
        message=message,
        responseCard=response_card,
    )


def confirm_intent(
        session_attributes: dict, intent_name: str, slots: dict, message: Union[dict, str],
        response_card=None
):
    if type(message) == str:
        message = msg_text_content(message)

    return build_response(
        session_attributes, 'ConfirmIntent',
        slots=slots,
        intentName=intent_name, message=message, responseCard=response_card,
    )


def close_fullfilled(session_attributes, message, slots: dict = None):
    return close(session_attributes, 'Fulfilled', message, slots)


def msg_text_content(msg: str):
    return {
        'contentType': 'PlainText',
        'content': msg
    }


def close(session_attributes: dict, fulfillment_state: str, message: Union[dict, str], slots: dict = None):
    if type(message) == str:
        message = msg_text_content(message)
    if slots:
        for key, val in slots.items():
            session_attributes[key] = val

    return build_response(session_attributes, 'Close', slots=None, fulfillmentState=fulfillment_state, message=message)


def delegate(session_attributes, slots):
    return build_response(session_attributes, 'Delegate', slots=slots)


def build_response_card(title, subtitle, options) -> dict:
    """
    Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons.
    """
    buttons = None
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }
