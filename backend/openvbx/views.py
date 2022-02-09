import re
from datetime import timedelta
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_twilio.views import twilio_view
from twilio.twiml.voice_response import VoiceResponse, Dial
from utils_plus.utils import reverse_url

from app_settings.models import GeneralSettings
from openvbx import models, tasks, utils

PHONE_PATTERN = re.compile(r"^[\d+\-\(\) ]+$")


@twilio_view
def caller_voice_response_view(request, company_id):
    """Respond to incoming phone calls with a message"""
    # Start our TwiML response
    resp = VoiceResponse()

    generalsettings = get_object_or_404(GeneralSettings, id=company_id)
    # Read a message aloud to the caller
    resp.say(
        f"The company name is {generalsettings.company_name} and its E-mail ID is {generalsettings.company_email}",
        voice='alice'
    )

    return resp


@twilio_view
def twiml_voice_handler(request: WSGIRequest):
    """handle all outbound calls from TwiML Application"""
    resp = VoiceResponse()
    to_address = request.POST.get('To')
    company_id = request.POST['CompanyId']
    caller_id = utils.get_caller_id(company_id)
    if to_address:
        # dial the given number
        if PHONE_PATTERN.match(to_address):
            # check if the number given has only digits and format symbols
            dial = Dial(caller_id=caller_id)
            dial.number(to_address)
        else:
            # dial the browser
            client_name = utils.get_client_name(company_id)
            dial = Dial(
                caller_id=caller_id,
                action=f'{request.build_absolute_uri(str(reverse_url("openvbx:record_call_view", company_id)))}',
                timeout=15,
            )
            dial.client(client_name)
        resp.append(dial)
    else:
        resp.say("Thanks for calling!")
    return resp


@twilio_view
def record_call_view(request, company_id):
    """
        when the dialed party doesn't available or busy, this URL will be called. This will record the call and send it
        for transcription and works like a kind of VoiceMail implementation.
    Args:
        request:
        company_id:

    Returns:

    """
    last_call_status = request.POST['DialCallStatus'] if 'DialCallStatus' in request.POST else None
    resp = VoiceResponse()

    # if the call was answered just end the call. Otherwise record it.
    if last_call_status not in {'completed', 'answered'}:
        # greet customer
        voicemailconfig, created = models.VoiceMailConfig.objects.get_or_create(generalsettings_id=company_id)
        if voicemailconfig.use_audio:
            resp.play(voicemailconfig.greeting_voice.url)
        else:
            resp.say(f'{voicemailconfig.greeting_message}. Press the star key when finished.')

        recording_handler_url = request.build_absolute_uri(
            str(reverse_url("openvbx:handle_recording_view", company_id)))
        # Use <Record> to record the caller's message
        resp.record(
            finish_on_key='*',
            action=recording_handler_url,
            max_length=120,
        )

    # End the call with <Hangup>
    resp.hangup()
    return resp


@twilio_view
def handle_recording_view(request, company_id):
    # store voicemail
    voicemail = models.VoiceMail()
    voicemail.generalsettings = get_object_or_404(GeneralSettings, id=company_id)
    callsid = request.POST.get('CallSid')
    if not callsid:
        raise Http404
    voicemail.callsid = callsid
    voicemail.from_caller_id = request.POST.get('From')
    voicemail.to_caller_id = request.POST.get('To')
    voicemail.recording_url = request.POST.get("RecordingUrl")
    voicemail.recordingsid = request.POST.get('RecordingSid')
    duration = str(request.POST.get('RecordingDuration'))
    duration = int(duration) if duration.isdigit() else 0
    voicemail.duration = timedelta(seconds=duration)
    voicemail.save()

    # say thanks response
    resp = VoiceResponse()
    resp.say("Thanks your message will be notified.")
    resp.say("Goodbye.")

    # start async task
    tasks.save_voicemail_and_transcribe(voicemail.id)

    return resp
