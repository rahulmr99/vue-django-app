import re
from django_twilio.decorators import twilio_view
from twilio.twiml import TwiML
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Dial, Say, Gather
from typing import Union
from utils_plus.utils import reverse_url

from lexbot.helpers.request_mappers import AppointmentHandler
from lexbot.models import CallerInfoQueue, VoiceBotConfig, LexSessionAttrsStore
from openvbx.utils import get_client_name
from .decorators import jwt_twilio_view
from .utils import get_bot_response

EMAIL_RE = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                       "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                       "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))


@jwt_twilio_view
def sms_bot_view(request, company_id: str):
    """
        gets called when the twilio number receives an incoming SMS.
        It connects with AWS lex bot to parse user's intent and creates appointment accordingly.
    Args:
        request:
        company_id:

    Returns:
        MessagingResponse:

    Notes:
        check tests.py for sample twilio request parameters
    """

    resp = MessagingResponse()
    text = request.POST['Body']
    # parse phone numbers
    provider_number, phonenumber, country = (request.POST['To'],
                                             request.POST['From'],
                                             request.POST.get('FromCountry'),)

    # we are getting the stored session attributes as Lex no longer saves client's session attributes
    user_id = phonenumber[1:]  # remove + symbol
    session_store = LexSessionAttrsStore.get(user_id)

    message = None
    # check whether the body contains only email address. else redirect to bot  and return its response
    if session_store is None:
        if EMAIL_RE.search(text):
            # check if this is within a lex conversation by checking the session attribute entry
            email_id = EMAIL_RE.search(text).group()
            appointmenthandler = AppointmentHandler(company_id,
                                                    providerPhoneNumber=request.POST['To'],
                                                    callerPhoneNumber=request.POST['From'],
                                                    callerCountry=request.POST.get('FromCountry'))

            # save email ID
            if appointmenthandler.customer_account and not appointmenthandler.customer_account.email:
                appointmenthandler.customer_account.email = email_id
                appointmenthandler.customer_account.save()

            message = "Thanks, we'll see you soon!"

        else:
            # create a session store and start conversation
            session_store = LexSessionAttrsStore.create(user_id=user_id)

    if not message:
        try:
            bot_response = get_bot_response(
                phonenumber[1:],
                request.POST['Body'],
                session_store,

                # session attrs
                callerPhoneNumber=phonenumber,
                callerCountry=country,
                company_id=company_id,
                providerPhoneNumber=provider_number,
            )
            # Return message returned from Lex
            message = bot_response.message
        except Exception:
            from lexbot.ravenclient import raven_client
            # call raven with this exception or log to django mail
            raven_client.captureException()
            message = "Application error."

    resp.message(message)
    return resp


AWS_CONNECT_BOOK_NUMBER = '+17029847578'
AWS_CONNECT_RESCHEDULE_NUMBER = '+17029795731'
AWS_CONNECT_CANCEL_NUMBER = '+17025221684'

VOICE_GET_BOOKING_PHONE_NUMBER_URL = "https://s3.amazonaws.com/bookedfusion.com/checks+phone+number+audios/first+response+if+it+doesn't+recognize+their+number.mp3"
VOICE_RETRY_BOOKING_PHONE_NUMBER_URL = "https://s3.amazonaws.com/bookedfusion.com/checks+phone+number+audios/2nd+response+if+it+still+doesn't+recognize+their+number.mp3"
VOICE_UNABLE_GETTING_BOOKING_PHONE_NUMBER_URL = "https://s3.amazonaws.com/bookedfusion.com/checks+phone+number+audios/3rd+response+if+doesn't+recognize+number+it+will+reroute+them.mp3"


def redirect_to_browser(request, company_id) -> Dial:
    url = request.build_absolute_uri(str(reverse_url("openvbx:record_call_view", company_id)))
    dial = Dial(action=f'{url}')
    dial.client(get_client_name(company_id))
    return dial


def redirect_to_customer_support(request, company_id) -> Dial:
    voicebotconfig, _ = VoiceBotConfig.objects.get_or_create(generalsettings_id=company_id)

    # resp.say('Redirecting to customer care')
    if voicebotconfig.redirect_to_browser:
        return redirect_to_browser(request, company_id)

    return Dial(number=voicebotconfig.redirect_telephone_number)


def redirect_to_cancel_appointment(appointmenthandler: AppointmentHandler) -> TwiML:
    msg = appointmenthandler.check_appointment_cancel_action()
    if msg:  # the appointment can't be cancelled and say the reason
        if 'reschedule' in msg:
            return Dial(number=AWS_CONNECT_RESCHEDULE_NUMBER)
        else:
            return Say(msg)
    else:  # forward to cancel number so that user can cancel by answering bot
        return Dial(number=AWS_CONNECT_CANCEL_NUMBER)


def redirect_to_reschedule_appointment() -> TwiML:
    return Dial(number=AWS_CONNECT_RESCHEDULE_NUMBER)


def redirect_to_cancel_or_reschedule_appointment(infoq: CallerInfoQueue, appointment: AppointmentHandler) -> TwiML:
    if infoq.want_rescheduling:
        return redirect_to_reschedule_appointment()

    else:  # cancel
        return redirect_to_cancel_appointment(appointment)


def get_phone_number_from_request(request, company_id) -> Union[TwiML, None]:
    """helper method"""
    if 'Digits' not in request.POST:
        return Say('No Digits were entered')

    phone_number = request.POST['Digits']
    phone_number = phone_number.strip('*')

    appointmenthandler = AppointmentHandler(
        company_id,
        callerPhoneNumber=phone_number,
        callerCountry=request.POST.get('FromCountry'),
        providerPhoneNumber=request.POST['To']
    )
    if appointmenthandler.customer_account:
        customer_number = request.POST['From']
        appointmenthandler.customer_account.add_cusomer_number(customer_number)
        infoq = CallerInfoQueue.get_caller_info(customer_number, delete=False)
        return redirect_to_cancel_or_reschedule_appointment(infoq, appointmenthandler)


@twilio_view
def retry_gathering_user_phone_number(request, company_id):
    resp = VoiceResponse()

    resp_for_req = get_phone_number_from_request(request, company_id)
    if resp_for_req:
        resp.append(resp_for_req)
    else:
        resp.play(VOICE_UNABLE_GETTING_BOOKING_PHONE_NUMBER_URL)
        resp.append(redirect_to_customer_support(request, company_id))
    return resp


@twilio_view
def gather_user_phone_number(request, company_id):
    resp = VoiceResponse()

    resp_for_req = get_phone_number_from_request(request, company_id)
    if resp_for_req:
        resp.append(resp_for_req)
    else:
        resp.play(VOICE_RETRY_BOOKING_PHONE_NUMBER_URL)
        url = request.build_absolute_uri(str(reverse_url("lexbot:retry_gathering_user_phone_number", company_id)))
        resp.gather(finish_on_key='*', action=url)

    return resp


@twilio_view
def get_voice_bot_user_choice(request, company_id: str):
    """Twilio's request to our app should include already gathered digits, process them."""
    resp = VoiceResponse()

    if 'Digits' not in request.POST:
        return resp.say('No Digits were entered')

    infoq = CallerInfoQueue.save_from_request(request, company_id)

    # <Say> a different message depending on the caller's choice
    if infoq.want_booking:  # book
        resp.dial(AWS_CONNECT_BOOK_NUMBER)

    elif infoq.want_help:  # customer support
        resp.append(redirect_to_customer_support(request, company_id))

    elif infoq.want_rescheduling or infoq.want_cancelling:  # reschedule/cancel
        appointmenthandler = AppointmentHandler(company_id,
                                                providerPhoneNumber=infoq.provider_number,
                                                callerPhoneNumber=infoq.caller_number,
                                                callerCountry=infoq.caller_country)

        if appointmenthandler.customer_account:
            resp.append(redirect_to_cancel_or_reschedule_appointment(infoq, appointmenthandler))
        else:
            # if number is not recognised then play audio and ask user to input phone number that they used to book
            resp.play(VOICE_GET_BOOKING_PHONE_NUMBER_URL)
            url = request.build_absolute_uri(str(reverse_url("lexbot:gather_user_phone_number", company_id)))
            resp.gather(finish_on_key='*', action=url)
    else:
        # If the caller didn't choose 1-4, apologize and disconnet the call
        resp.say("Sorry, I don't understand that choice.")
    return resp


@twilio_view
def voice_bot_view(request, company_id: str):
    """
        gets called when the twilio number receives an incoming Call. It redirects call to AWS Connect.
        Which then uses Lex for interactive reply.
    Args:
        request:
        company_id:

    Returns:
        XmlResponse:

    Notes:
        check tests.py for more details
    """

    voicebotconfig, _ = VoiceBotConfig.objects.get_or_create(generalsettings_id=company_id)

    # get user button press
    _handler_url = request.build_absolute_uri(str(reverse_url("lexbot:get_voice_bot_user_choice", company_id)))
    gather = Gather(num_digits=1, action=_handler_url)
    # play custom welcome message configured
    if voicebotconfig.use_audio and voicebotconfig.greeting_voice:
        gather.play(voicebotconfig.greeting_voice.url)
    else:
        gather.say(voicebotconfig.greeting_message)

    resp = VoiceResponse()
    resp.append(gather)

    return resp
