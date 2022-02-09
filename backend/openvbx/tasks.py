import logging
import requests
import shutil
import speech_recognition as sr
from datetime import timedelta
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from twilio.rest import Client
from zappa.async import task

from .models import *
from app_settings.models import TwilioAccount

logger = logging.getLogger(__file__)


@task
def save_voicemail_and_transcribe(voicemail_id):
    """
        save audio from twilio storages and transcribe with google APIs
    """
    logger.info(f'save_voicemail_and_transcribe for voicemail id: {voicemail_id}')
    voicemail: VoiceMail = VoiceMail.objects.filter(id=voicemail_id).first()
    if not voicemail or not voicemail.recording_url:
        return

    # download mp3
    audio_filename = f'voicemail.{voicemail.recordingsid}.mp3'
    resp = requests.get(f'{voicemail.recording_url}.mp3', stream=True)
    audio_file = NamedTemporaryFile(delete=True)
    shutil.copyfileobj(resp.raw, audio_file)
    audio_file.flush()
    del resp

    # save it to model
    voicemail.recorded_file.save(audio_filename, File(audio_file))
    voicemail.save()

    # run transcription
    transcribe_audio(voicemail)

    # delete original recording from twilio
    requests.delete(voicemail.recording_url)


def transcribe_audio(voicemail):
    # download as wav
    resp = requests.get(f'{voicemail.recording_url}.wav', stream=True)
    audio_file = NamedTemporaryFile(delete=True)
    shutil.copyfileobj(resp.raw, audio_file)
    audio_file.flush()
    del resp

    # transcribe using speech recognition
    r = sr.Recognizer()
    with sr.AudioFile(audio_file.name) as source:
        # cut only first 60 seconds
        audio = r.record(source, duration=60)  # read the entire audio file

        with open(settings.GOOGLE_SERVICE_ACC_JSON) as f:
            auth = f.read()

        voicemail.transcription_text = r.recognize_google_cloud(audio, credentials_json=auth)

    voicemail.save()


# @periodic_task(run_every=timedelta(hours=24))
def delete_older_voicemails():
    logger.info('Running tasks to delete older voicemails than 30 days')

    dt = timezone.now() - timedelta(30)
    for voicemail in VoiceMail.objects.filter(created__lt=dt, recorded_file__isnull=False):
        if voicemail.recorded_file:
            voicemail.recorded_file.delete()


@task
def _send_twilio_sms(to: str, body: str, from_number: str = None):
    """Note: Should use send_sms instead of using this directly"""
    from .utils import get_twilio_client
    
    # NOTE: Each twilio subaccounts needs to use their own credentials
    # like auth_token, sid inorder to access the twilio apis
    try:
        twilio_account = TwilioAccount.objects.get(booked_fusion_number=from_number)
    except TwilioAccount.DoesNotExist:
        twilio_account = None

    if twilio_account:
        client = Client(twilio_account.account_sid, twilio_account.auth_token)
        from_number = from_number or settings.TWILIO_DEFAULT_CALLERID
        message = client.messages.create(to, from_=from_number, body=body)
        logger.info(f'Send Twilio SMS to {to}')
        return str(message)
        
    elif settings.TWILIO_DEFAULT_CALLERID:
        client: Client = get_twilio_client()
        from_number = settings.TWILIO_DEFAULT_CALLERID
        message = client.messages.create(to, from_=from_number, body=body)
        logger.info(f'Send Twilio SMS to {to}')

    