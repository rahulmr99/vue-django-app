from collections import namedtuple

import logging
import requests
import threading
from django.conf import settings
from twilio.rest import Client

from app_settings.models import TwilioAccount

log_sms = logging.getLogger('sms')
thread_locals = threading.local()


def get_client_name(company_id):
    return f"jenny-{company_id}"


SMS_MOCK = namedtuple('SMS', ('body', 'from_', 'to'))


def get_twilio_client():
    if not hasattr(thread_locals, 'client'):
        thread_locals.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    return thread_locals.client


def get_sms_outbox():
    """used in tests"""
    if not hasattr(thread_locals, 'sms_outbox'):
        thread_locals.sms_outbox = []
    return thread_locals.sms_outbox


def _mock_sending_sms(to: str, body: str, from_number: str = None):
    msg = SMS_MOCK(body, from_number, to)
    outbox = get_sms_outbox()
    outbox.append(msg)
    return msg


def send_sms(to: str, body: str, from_number: str = None):
    """send SMS using Twilio API or mock it when configured as settings.MOCK_SMS=True"""
    if getattr(settings, 'MOCK_SMS', False):
        message = _mock_sending_sms(to, body, from_number)
    else:
        from .tasks import _send_twilio_sms
        message = _send_twilio_sms(to=to, body=body, from_number=from_number)

    log_sms.info(message)
    return message


def send_telegram(message):
    """Send Message to Telegram channel."""
    return requests.post(
        'https://api.telegram.org/bot272606808:AAFkyO_YmBswOLeNZ2AV3WsYeaeTrW6yPDU/sendMessage',
        data={
            'chat_id': '-172968462',
            'text': message
        }
    )


def get_booked_fusion_number(generalsettings_id):
    booked_fusion_number = (
        TwilioAccount.objects.filter(generalsettings_id=generalsettings_id, sid__isnull=False).exists()
    )
    return {'is_booked_fusion_number': booked_fusion_number}


def get_caller_id(generalsettings_id):
    """for the given company ID return the Phone number if available otherwise return the default number from settings"""
    return (
               TwilioAccount.objects
                   .filter(generalsettings_id=generalsettings_id, sid__isnull=False)
                   .values_list('booked_fusion_number', flat=True).first()
           ) or settings.TWILIO_DEFAULT_CALLERID


def send_pusher_notification(title: str, channel: str, msg: dict):
    import pusher
    client = pusher.Pusher(
        app_id='533625',
        key='4010826535e9b939f154',
        secret='42be04e8e70131eab672',
        cluster='ap2',
    )
    client.trigger(title, channel, msg, )
