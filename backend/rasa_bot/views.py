"""
Rasa bot views 
"""
import json
import pytz
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rasa_bot.models import RasaBotUserSession
from app_settings.models import GeneralSettings

import rest_framework.decorators
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

import lexbot.utils
from lexbot import msgs
from lexbot.handlers import utils
from lexbot.helpers.request_mappers import AppointmentHandler
from calendar_manager.models import CalendarDb
from authentication_user.models import Account
from app_settings.models import TwilioAccount
from openvbx.utils import get_booked_fusion_number
from rasa_bot.utils import send_fallback_notification

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from twilio.rest import Client


@csrf_exempt
def rasa_bot_user(request):
    """
    Check if its new user or not. If its new user add to db
    """
    if request.method == 'POST':
        provider_number = request.POST.get('to')
        customer = request.POST.get('from')
        country = request.POST.get('fromCountry')
        user_exist = False
        try:
            twilio_account = TwilioAccount.objects.get(
                booked_fusion_number=provider_number)
            provider = Account.objects.filter(
                generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()
            appt = CalendarDb.objects.filter(
                users_provider=provider, users_customer__phone=customer[2:], users_customer__is_provider=False)

            if appt.exists():
                name = appt.last().users_customer.name
                email = appt.last().users_customer.email
                user_exist = True
            else:
                customer = Account.objects.get(phone=customer[2:])
                name = customer.name
                email = customer.email
                user_exist = True
        except:
            name = email = None
            user_exist = False

        return JsonResponse({'user_exist': user_exist, 'fname': name, 'email': email})
    else:
        return JsonResponse({'response_data': "GET method not allowed"})


@csrf_exempt
def check_timeslot_available(request):
    """
    Check user given timeslot is available
    """
    timeslot_avilable = None

    if request.method == 'POST':
        timeslot = request.POST.get('timeSlot')
        provider = request.POST.get('provider')
        customer = request.POST.get('customer')

        user = utils.get_user(customer)
        provider_number = provider[2:]
        customer_number = customer[2:]
        provider, customer = utils.get_provider_and_customer(
            provider, customer_number)
        given_book_date = utils.parse_datetime(timeslot).replace(tzinfo=None)
        # given_book_date = utils.parse_datetime(timeslot)

        msg_check_valid_date = utils.check_valid_date_time(
            given_book_date, provider)
        msg_check_dt_available, timeslot_avilable = utils.check_date_time_available(
            given_book_date, provider)

        if msg_check_valid_date:
            result = msg_check_valid_date

        elif msg_check_dt_available:
            result = msg_check_dt_available

        else:
            result = None

        return JsonResponse({'response_data': result, 'timeslot_avilable': timeslot_avilable})
    else:
        return JsonResponse({'response_data': "GET method not allowed"})


def check_user_exist(provider_number, customer):
    try:
        twilio_account = TwilioAccount.objects.get(
            booked_fusion_number=provider_number)
        provider = Account.objects.filter(
            generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()
        appt = CalendarDb.objects.filter(
            users_provider=provider, users_customer__phone=customer[2:], users_customer__is_provider=False)

        if appt.exists():
            return True
        else:
            customer = Account.objects.get(phone=customer[2:])
        return True
    except:
        return False


@csrf_exempt
def rasa_bot_book_appt(request):
    """
    Book appointment if timeslot available
    """
    if request.method == 'POST':

        timeslot = request.POST.get('timeSlot')
        provider = request.POST.get('provider')
        customer = request.POST.get('customer')
        name = request.POST.get('name')
        email = request.POST.get('userEmail')
        patient_type = request.POST.get('patientType')
        user_already_exit = check_user_exist(provider, customer)

        # If user is already exit then change patient service to return patient
        if not user_already_exit:
            return_or_new_patient = 0 if patient_type == 'true' else 1
        else:
            return_or_new_patient = 1

        booking_status = False
        kwargs = {"email": email}

        try:
            name_list = name.split()
            first_name = name_list[0]
            last_name = name_list[1]
        except (IndexError, AttributeError):
            first_name = name
            last_name = name

        # Add customer number also in the rasa bot table
        user, created = RasaBotUserSession.objects.get_or_create(
            user_id=customer[2:])

        if created:
            user.from_no = customer[2:]
            user.to_no = provider[2:]
            user.save()

        user_account = utils.get_user_account(user)

        provider_number = provider[2:]
        customer_number = customer[2:]

        provider, customer = utils.get_provider_and_customer(
            provider, customer_number)
        given_book_date = utils.parse_datetime(timeslot).replace(tzinfo=None)

        # Check the given date is correct and chec if its avalibale or not
        msg_check_valid_date = utils.check_valid_date_time(
            given_book_date, provider)
        msg_check_dt_available, timeslot_avilable = utils.check_date_time_available(
            given_book_date, provider)

        if msg_check_valid_date:
            result = msg_check_valid_date

        elif msg_check_dt_available:
            result = msg_check_dt_available

        else:
            result = None

        if result:
            return JsonResponse({'response_data': result, 'timeslot_avilable': timeslot_avilable})

        company_id = provider.generalsettings_id if provider else None

        if not customer:
            if Account.registered_with_email_id(email, company_id):
                message = "Please provide another E-mail ID. This is already registered with us."
                return JsonResponse({'response_data': message})

        calender_db = CalendarDb.add_or_reschedule_appointment(
            start_time=given_book_date,
            provider=provider,
            customer=lexbot.utils.get_or_create_customer_account(
                customer,
                customer_number,
                provider.generalsettings_id,
                user_account.name if user_account else first_name,
                user_account.last_name if user_account else last_name,
                **kwargs
            ),
            service=(lexbot.utils.get_service(provider, str(return_or_new_patient))
                     ),
            appointment_id=None,
            rasa_bot=True
        ),

        if isinstance(calender_db, tuple) and not calender_db[0]:
            return JsonResponse({'response_data': "Slot is already booked"})

        try:
            message = msgs.THANKS_NOTE_AFTER_BOOK_BOTKIT.format(
                time=utils.get_time(calender_db[0].start_datetime) if utils.get_time(
                    calender_db[0].start_datetime) else '',
                day=calender_db[0].start_datetime.strftime("%A"),
                date=calender_db[0].start_datetime.strftime("%d %b"),
                customer_name=calender_db[0].users_customer.name,
            ),
            message = message[0]
            booking_status = True

        except IndexError:
            message = "Hmm, I'm having trouble to booking appointment"

        return JsonResponse({'response_data': message, 'booking_status': booking_status})

    return JsonResponse({'response_data': "GET method not allowed"})


@csrf_exempt
def reschedule_appt(request):

    if request.method == 'POST':
        timeslot = request.POST.get('timeSlot')
        provider = request.POST.get('provider')
        customer = request.POST.get('customer')
        is_reschedule = request.POST.get('reschedule')
        new_or_return_patient = request.POST.get('newOrReturnPatient')
        user_exist = False
        status = False

        if timeslot:
            given_book_date = utils.parse_datetime(
                timeslot).replace(tzinfo=None)

        user = utils.get_user(customer[2:])

        provider_number = provider[2:]
        customer_number = customer[2:]

        provider, customer = utils.get_provider_and_customer(
            provider, customer_number)

        # Check the given date is correct and chec if its avalibale or not
        msg_check_valid_date = utils.check_valid_date_time(
            given_book_date, provider)
        msg_check_dt_available, timeslot_avilable = utils.check_date_time_available(
            given_book_date, provider)

        if msg_check_valid_date:
            result = msg_check_valid_date

        elif msg_check_dt_available:
            result = msg_check_dt_available

        else:
            result = None
            status = True

        if result:
            return JsonResponse({'response_data': result, 'timeslot_avilable': timeslot_avilable, 'status':status})

        user_exist = True if user else False

        if not user_exist:

            msg = "I’m sorry I can’t seem to find your appointment from the number you texted in with. Please reply back with just the number we have on file with area code."

            return JsonResponse({'response_message': msg, 'status':status})

        else:
            user_account = utils.get_user_account(user)

            if not user_account:
                return JsonResponse({'response_message': "I'm sorry. I can`t find your appointment from the phone number you texted in.\
	        To book new appointment, just say day and time with A.M or P.M after time.", 'status':status})

            appointment_obj = utils.get_appointment(user, user_account, provider)
            fname = user_account.name if user_account else None

            if is_reschedule:

                return_or_new_patient = 0 if new_or_return_patient else 1
                kwargs = {}

                calender_db = CalendarDb.add_or_reschedule_appointment(
                    start_time=given_book_date,
                    provider=provider,
                    customer=lexbot.utils.get_or_create_customer_account(
                        customer,
                        customer_number,
                        provider.generalsettings_id,
                        user_account.name if user_account else '',
                        user_account.last_name if user_account else '',
                        **kwargs
                    ),
                    service=(lexbot.utils.get_service(provider, str(return_or_new_patient))
                             ),
                    appointment_id=appointment_obj.id if appointment_obj else None,
                    rasa_bot=True
                ),

                if not calender_db:
                    return JsonResponse({'response_message': "Slot is already booked", 'status':status})

                try:
                    message = msgs.THANKS_NOTE_AFTER_RESCHEDULE.format(
                        time=utils.get_time(calender_db[0].start_datetime) if utils.get_time(
                            calender_db[0].start_datetime) else '',
                        day=calender_db[0].start_datetime.strftime("%A"),
                        date=calender_db[0].start_datetime.strftime("%d %b"),
                    ),
                    message = message[0]
                    status = True
                except IndexError:
                    message = "Hmm, I'm having trouble to reschedule appointment"

                return JsonResponse({'response_message': message,'status':status})

            msg = utils.msg_for_reschedule_appt(appointment_obj, None)

            if msg:
                return JsonResponse({'response_message': msg, 'fname': fname, 'status':status})
    else:
        return JsonResponse({'response_message': "GET method not allowed"})


@csrf_exempt
def cancel_appt(request):

    if request.method == 'POST':
        
        provider = request.POST.get('provider')
        customer = request.POST.get('customer')
        is_cancel = request.POST.get('cancel')
        new_or_return_patient = request.POST.get('newOrReturnPatient')
        user_exist = False
        status = False

        user = utils.get_user(customer[2:])

        provider_number = provider[2:]
        customer_number = customer[2:]

        provider, customer = utils.get_provider_and_customer(
            provider, customer_number)

        user_exist = True if user else False

        if not user_exist:
            msg = "I'm sorry I don't recognize the number you are texting in with.\
	            Either text in from that number we have on file or call us to reschedule."

            return JsonResponse({'response_message': msg})

        user_account = utils.get_user_account(user)
        fname = user_account.name if user_account else None

        if not user_account:
            return JsonResponse({'response_message': "I'm sorry. I can`t find your appointment from the phone number you texted in.\
	        To book new appointment, just say day and time with A.M or P.M after time."})

        appointment_obj = utils.get_appointment(user, user_account, provider)
        appt_instance = AppointmentHandler(
            provider.generalsettings_id, provider_number, customer_number)

        if is_cancel == 'true':

            if not appointment_obj:
                msg = msgs.APPOINTMENT_NOT_FOUND

            # elif appt_instance.calendar_appointment.is_cancelable:
            #     msg = msgs.CANCELLATION_POLICY_24

            elif not appt_instance.calendar_appointment.is_cancelable(provider):
                msg = msgs.CANCELLATION_POLICY_24

            else:
                appt_instance.calendar_appointment.cancel_appointment()
                msg = msgs.APPOINTMENT_CANCELLED
                status = True
        else:

            if appt_instance.calendar_appointment.is_cancelable(provider):
                msg = appt_instance.get_customer_confirmation_for_cancel()
                status = True
            else:
                msg = msgs.CANCELLATION_POLICY_24

        return JsonResponse({'response_message': msg, 'fname': fname, 'status':status})


@csrf_exempt
def generate_access_token_bot(request):

    if request.method == 'POST':
        provider_number = request.POST.get('provider')

        try:
            twilio_account = TwilioAccount.objects.get(
                booked_fusion_number=provider_number)
            user_account = Account.objects.filter(
                generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()
        except Account.DoesNotExist:
            return JsonResponse({'response_message': "User does not exist"})

        identity = user_account.email
        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY
        api_secret = settings.TWILIO_API_SECRET

        # required for Chat grants
        service_sid = settings.TWILIO_SERVICE_SID
        identity = identity

        token = AccessToken(account_sid, api_key,
                            api_secret, identity=identity)
        chat_grant = ChatGrant(service_sid=service_sid)
        token.add_grant(chat_grant)
        return JsonResponse({"token": token.to_jwt().decode("utf-8")})

    else:
        return JsonResponse({'response_message': "Not allowed"})


@csrf_exempt
def get_provider_email(request):

    if request.method == 'POST':
        provider = request.POST.get('provider')

        try:
            twilio_account = TwilioAccount.objects.get(
                booked_fusion_number=provider)
            account = Account.objects.filter(
                generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()
        except Account.DoesNotExist:
            return JsonResponse({'user_exist': False})
        except TwilioAccount.DoesNotExist:
            return JsonResponse({'user_exist': False})

        return JsonResponse({'user_exist': True, 'email': account.email})

    else:
        return JsonResponse({'response_message': "GET method not allowed"})


@csrf_exempt
def send_sms_to_user(request):
    """
    Send sms to user when a message is send to the chat
    """
    if request.method == 'POST':
        channel_sid = request.POST.get('ChannelSid')
        from_email = request.POST.get('ClientIdentity')
        body = request.POST.get('Body')

        try:
            provider = Account.objects.get(email=from_email)
        except Account.DoesNotExist:
            provider = None

        try:
            twilio_account = TwilioAccount.objects.filter(
                generalsettings=provider.generalsettings).first()
        except TwilioAccount.DoesNotExit:
            twilio_account = None

        if twilio_account:
            account_sid = twilio_account.account_sid
            auth_token = twilio_account.auth_token
            service_id = twilio_account.service_id
        else:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            service_id = settings.TWILIO_SERVICE_SID
            twilio_account = provider

        client = Client(account_sid, auth_token)
        members = client.chat.services(service_id) \
            .channels(channel_sid) \
            .members \
            .list()

        for each_member in members:
            try:
                if each_member.identity != twilio_account.booked_fusion_number:
                    message = client.messages.create(
                        from_=twilio_account.booked_fusion_number,
                        body=body,
                        to=each_member.identity
                    )
            except:
                pass

        return JsonResponse({'result': "success"})

@csrf_exempt
def get_provider_timezone(request, provider_number):
    """
    Return provider timezone 
    """

    # try:
    #     user_phone = phone_no[1:]
    # except Exception as e:
    #     return JsonResponse({'response_message': e})
    try:
        twilio_account = TwilioAccount.objects.get(
            booked_fusion_number=provider_number)
        provider = Account.objects.filter(
            generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()
    except Account.DoesNotExist:
        return JsonResponse({'response_message': "This phone number does not assosiated with any account"})

    if provider:
        return JsonResponse({'timezone': provider.timezone})
    else:
        return JsonResponse({'response_message': "This phone number does not assosiated with any account"})


@csrf_exempt
def send_fallback_email(request):
    """
    Send email to provider when bot doesn't understand the intent
    """
    if request.method == 'POST':
        provider = request.POST.get('provider')
        customer = request.POST.get('customer')
        user_email = request.POST.get('userEmail')
        customer_name = request.POST.get('name')
        fallback_message = request.POST.get('msg')

        try:
            twilio_account = TwilioAccount.objects.get(
                booked_fusion_number=provider)
            provider_account = Account.objects.filter(
                generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()

        except TwilioAccount.DoesNotExist:
            twilio_account = None

        except Account.DoesNotExist:
            provider_account = None

        if provider_account:
            # Send mail to company email instead email used to signup
            if provider_account.generalsettings:
                company_email = provider_account.generalsettings.company_email
            else:
                company_email = provider_account.email if provider_account else None

            send_fallback_notification(
                company_email, customer, fallback_message)

        return JsonResponse({'response_message': True})


@csrf_exempt
def get_provider_phone_number(request):
    body = json.loads(request.body.decode("utf-8"))
    generalsettings_id = body.get('generalsettings_id')
    twilio_acc = TwilioAccount.objects.filter(generalsettings_id=generalsettings_id, sid__isnull=False)
    if twilio_acc.exists():
        number = twilio_acc[0].booked_fusion_number
        return JsonResponse({'provider_number':number})
    else:
        return JsonResponse({'provider_number':None})


@csrf_exempt
def get_pre_booking_date(request):
    """
    Check if there any latest appt
    """
    customer = request.POST.get('customer')
    provider = request.POST.get('provider')

    provider_number = provider[2:]
    customer_number = customer[2:]

    user = utils.get_user(customer[2:])

    provider, customer = utils.get_provider_and_customer(
            provider, customer_number)

    user_account = utils.get_user_account(user)

    if not user_account:
        return JsonResponse({'response_message': "I'm sorry. I can`t find your appointment from the phone number you texted in.\
        To book new appointment, just say day and time with A.M or P.M after time.", "pre_booking_date":False})

    appointment_obj = utils.get_appointment(user, user_account, provider)

    if appointment_obj:
        
        if provider:
            tzname = 'US/Eastern' if provider.timezone == 'EST' else provider.timezone
            tz_obj = pytz.timezone(tzname)
            appt_date = appointment_obj.start_datetime.astimezone(tz_obj)
        
            year = appt_date.strftime("%Y")
            month = appt_date.strftime("%m")
            day = appt_date.strftime("%d")
            appt_date = year+"-"+month+"-"+day
            
            return JsonResponse({'response_message':"Success", "pre_booking_date":appt_date})
    
    if appointment_obj:
        return JsonResponse({'response_message':"Failed", "pre_booking_date":False})
    

@api_view()
@rest_framework.decorators.list_route(methods=['get'], permission_classes=[IsAuthenticated, ])
def generate_access_token(request):
    """
    return access token for twilio JS SDK client
    """
    if request.method == 'GET':
        username = request.user.username
        try:
            user_account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return JsonResponse({"response_message": "User does not exit"})

        # Each twilio subaccount have its own chat service id we need to pass these
        # when create a accesstoken for chat
        try:
            twilio_account = TwilioAccount.objects.filter(
                generalsettings=user_account.generalsettings).first()
        except TwilioAccount.DoesNotExist:
            twilio_account = None

        identity = user_account.email

        # required for Chat grants
        if twilio_account:
            account_sid = twilio_account.account_sid
            service_sid = twilio_account.service_id
            api_key = twilio_account.api_key
            api_secret = twilio_account.api_key_secret
        else:
            account_sid = settings.TWILIO_ACCOUNT_SID
            service_sid = settings.TWILIO_SERVICE_SID
            api_key = settings.TWILIO_API_KEY
            api_secret = settings.TWILIO_API_SECRET

        token = AccessToken(account_sid, api_key,
                            api_secret, identity=identity)
        chat_grant = ChatGrant(service_sid=service_sid)
        token.add_grant(chat_grant)
        return JsonResponse({"token": token.to_jwt().decode("utf-8")})

    else:
        return JsonResponse({'response_message': "Method not allowed"})


@api_view()
@rest_framework.decorators.list_route(methods=['get'], permission_classes=[IsAuthenticated, ])
def get_upcoming_appts(request, phone_no):
    """
    Get latest appt of patient
    """
    if request.method == 'GET':
        try:
            user_phone = phone_no[1:]
        except Exception as e:
            return JsonResponse({'response_message': e})

        try:
            user_account = Account.objects.get(phone=user_phone)
        except Account.DoesNotExist:
            user_account = None

        try:
            username = request.user.username
            provider = Account.objects.get(phone=user_phone)
            # twilio_account = TwilioAccount.objects.get(booked_fusion_number=phone_no)
            # provider = Account.objects.filter(generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()
        except Account.DoesNotExist:
            provider = None

        if user_account:
            upcoming_appt_date = user_account.get_next_appoinment(provider)
            name = user_account.name+' '+user_account.last_name
            is_new_patient = False
        else:
            upcoming_appt_date = None
            name = phone_no
            is_new_patient = True

        # Convert the date into string format
        if upcoming_appt_date:
            month = upcoming_appt_date.strftime("%b")
            date = upcoming_appt_date.strftime("%d")
            time = upcoming_appt_date.strftime("%I:%M %p")
            upcoming_appt_date = month + " "+date+" - "+time

        return JsonResponse({'upcoming_appt_date': upcoming_appt_date, "name": name, "is_new_patient": is_new_patient})
    else:
        return JsonResponse({'response_message': "Method not allowed"})


@api_view()
@rest_framework.decorators.list_route(methods=['get'], permission_classes=[IsAuthenticated, ])
def get_ai_on_off_status(request, phone_no):
    if request.method == 'GET':
        try:
            user_phone = phone_no[1:]
        except Exception as e:
            return JsonResponse({'response_message': e})

        try:
            username = request.user.username
            provider = Account.objects.get(username=username)
            twilio_account = TwilioAccount.objects.get(
                generalsettings=provider.generalsettings)
            booked_fusion_number = twilio_account.booked_fusion_number

        except Account.DoesNotExist:
            provider = None

        except TwilioAccount.DoesNotExist:
            booked_fusion_number = None

        if booked_fusion_number:
            user_no = "+" + str(phone_no)
            provider_no = str(booked_fusion_number)
            data = {"user": user_no, "provider": provider_no}
            headers = {'Content-Type': 'application/json'}
            url = '{}/on_off'.format(settings.BOTKIT_SERVER_URL)
            response = requests.get(url, params=data, headers=headers)
            data = response.json()
            return JsonResponse({'response_message': data.get('toggle') if data.get('toggle', None) else data.get('msg', False)})
        else:
            return JsonResponse({'response_message': "Failed"})


@api_view(['POST'])
def toggle_ai(request):
    """
    Turn AI on/off feature
    """

    if request.method == 'POST':
        try:
            post_data = json.loads(request.body.decode("utf-8"))
            user_no = post_data['user']
            generalsettings_id = post_data['generalsettings_id']
            toggle = post_data['toggle']
            generalsettings_obj = GeneralSettings.objects.get(
                id=generalsettings_id)
            twilio_account = TwilioAccount.objects.filter(
                generalsettings=generalsettings_obj).first()
            # call node server for enable/disable AI
            user_no = "+" + str(user_no)
            provider_no = str(twilio_account.booked_fusion_number)
            data = json.dumps(
                {"user": user_no, "provider": provider_no, "toggle": str(toggle)})
            headers = {'Content-Type': 'application/json'}
            url = '{}/on_off'.format(settings.BOTKIT_SERVER_URL)
            response = requests.post(url, data=data, headers=headers)
            return JsonResponse({'response_message': True})
        except Exception as e:
            return JsonResponse({'response_message': str(e)})
        # data = response.json()


@api_view(['POST'])
def add_member_to_channel(request):
    """
    Add member to the twilio chat channel when FE try to add
    number using send new message feature
    """
    body = json.loads(request.body.decode("utf-8"))
    user_no = body.get('new_number')
    user_no = str(user_no)
    channel_id = body.get('channel_id')

    try:
        username = request.user.username
        provider = Account.objects.get(username=username)
        twilio_account = TwilioAccount.objects.get(
            generalsettings=provider.generalsettings)
        booked_fusion_number = twilio_account.booked_fusion_number

    except Account.DoesNotExist:
        provider = None
        twilio_account = None
    if provider and twilio_account:
        try:
            client = Client(twilio_account.account_sid, twilio_account.auth_token)
            client.chat.services(twilio_account.service_id).channels(channel_id).members.create(identity=user_no)
        except Exception as e:
            return JsonResponse({'response':str(e)})
    else:
        return JsonResponse({'response':False})

    return JsonResponse({'response':True})


@api_view(['POST'])
def check_phone_number_is_valid(request):
    """
    Check given number is valid or not by using twilio lookup api
    """
    body = json.loads(request.body.decode("utf-8"))
    user_no = body.get('phone_number')

    try:
        username = request.user.username
        provider = Account.objects.get(username=username)
        twilio_account = TwilioAccount.objects.get(
            generalsettings=provider.generalsettings)
        booked_fusion_number = twilio_account.booked_fusion_number

    except Account.DoesNotExist:
        provider = None

    except TwilioAccount.DoesNotExist:
        twilio_account = None

    if twilio_account:
        account_sid = twilio_account.account_sid
        auth_token = twilio_account.auth_token
        client = Client(account_sid, auth_token)
        
        # Twilio lookup return HTTP 404 status code if the numnber is not valid
        try:
            is_valid = client.lookups.phone_numbers(user_no).fetch(country_code='US')
        except Exception as e:
            is_valid  = None

        if not is_valid:
            content = {"status":"failed"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        content = {"status":"success"}
        return Response(content, status=status.HTTP_200_OK)
