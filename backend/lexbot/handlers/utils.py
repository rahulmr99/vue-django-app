""" --- Helper Functions --- """

import datetime
import pytz
import dateutil.parser

from django.http import JsonResponse

from collections import OrderedDict
from typing import Union, Dict, List
from calendar_manager.utils import check_breaks, filter_a_days_slots
from authentication_user.models import Account
from rasa_bot.models import RasaBotUserSession
from app_settings.models import TwilioAccount
from lexbot import msgs

TIME_FMT = '%-I:%M %p'
TIME_ZONE = 'America/New_York'
timezone = pytz.timezone(TIME_ZONE)
DAY_STRINGS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def parse_datetime(date: str) -> Union[datetime.datetime, None]:
    try:
        return dateutil.parser.parse(date)
    except (ValueError, TypeError):
        return None


DAY_STRINGS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def build_date_options(available_days: set):
    """
    Build a list of potential options for a given slot, to be used in responseCard generation.
    """
    options = []
    potential_date = datetime.date.today()
    while len(options) < 5:
        potential_date = potential_date + datetime.timedelta(days=1)
        if potential_date.isoweekday() in available_days:
            options.append({'text': '{}-{} ({})'.format(potential_date.month, potential_date.day,
                                                        DAY_STRINGS[potential_date.weekday()]),
                            'value': potential_date.strftime('%A, %B %d, %Y')})
    return options


def build_date_options_str(available_days: set) -> str:
    """
    Build a list of potential options for a given slot, to be used as plain text where response card is not supported
    """
    options = []
    potential_date = datetime.date.today()
    while len(options) < 5:
        potential_date = potential_date + datetime.timedelta(days=1)
        if potential_date.isoweekday() in available_days:
            options.append(potential_date.strftime('%A, %B %d, %Y'))
    return ", ".join(options)


def build_aptime_options():
    """
    Build a list of potential options for a given slot, to be used in responseCard generation.
    """
    options = [
        {
            "text": "Morning",
            "value": "Morning"
        },
        {
            "text": "Evening",
            "value": "Evening",
        },
    ]
    return options


def filter_time_slots(available_times: Dict[str, datetime.datetime]) -> List[str]:
    """return first three slots with interval of 30 mins"""
    times_available = []  # show users the first three time slots that with 30 mins gap in the slots
    times = list(available_times.keys())

    if len(times) and len(times_available) < 3:
        while len(times) and len(times_available) < 3:
            time_frmt = times.pop(0)
            if (len(times_available) == 0  # fill first value as it is
                        or
                        (len(times_available) < 3 and len(times) < 3)
                    ):
                times_available.append(time_frmt)
            else:  # otherwise select timeslot after 30 mins
                first_time = available_times[times_available[-1]]
                time_frmt_time = available_times[time_frmt]
                if (time_frmt_time - first_time) >= datetime.timedelta(minutes=30):
                    times_available.append(time_frmt)
    else:
        times_available = times

    return times_available

####################################################


def get_time(book_date):
    return book_date.strftime(TIME_FMT)


def get_user(customer):
    try:
        user = RasaBotUserSession.objects.get(user_id=customer)
    except RasaBotUserSession.DoesNotExist:
        user = None

    return user


def get_provider_and_customer(provider_number, customer_number):

    try:
        twilio_account = TwilioAccount.objects.get(
            booked_fusion_number=provider_number)
        provider = Account.objects.filter(
            generalsettings=twilio_account.generalsettings, is_provider=True).prefetch_related('services').first()
    except Account.DoesNotExist:
        provider = None

    try:
        customer = Account.objects.get(phone=customer_number)
    except Account.DoesNotExist:
        customer = None

    return provider, customer


def days_working_plan(booking_date, provider):
    """ Get working plan """
    return provider.workingplan_set.filter(day=booking_date.isoweekday()).get()


def is_beyond_working_time_selected(booking_date, provider):
    """when user tried to book out of the working hours"""
    days_working = days_working_plan(booking_date, provider)
    return days_working.end < booking_date.time()


def is_below_working_time_selected(booking_date, provider):
    """when user tried to book out of the working hours"""
    days_working = days_working_plan(booking_date, provider)
    return booking_date and days_working.start > booking_date.time()


def available_times(booking_date, provider):
    """ Return available times """
    from calendar_manager.models import CalendarDb

    # convert time to provider timezone
    tzname = provider.timezone if provider else 'US/Eastern'
    tzname = 'US/Eastern' if tzname == "EST" else tzname
    tz_obj = pytz.timezone(tzname)
    date = booking_date.astimezone(tz_obj)

    last_selected_time = date

    available_times = OrderedDict([
        (slot.strftime(TIME_FMT), slot)

        for slot in filter_a_days_slots(
            day=last_selected_time,
            providers_working_plan=days_working_plan(
                last_selected_time, provider),
            interval=provider.appointment_interval,
            providers_calendar_tasks=CalendarDb.objects.filter(
                users_provider=provider),
            providers_breaks=provider.breaks_set.all(),
            user=provider,
        )
        # filter only latest slots than last selected time in the given date
        if (((slot > last_selected_time) or (slot == last_selected_time)))
        # if the time is already filled, make sure that available time includes the selected slot time

    ])
    return available_times


def is_busy_day(booking_date, provider):
    """ Check whether any available slots in the given day """

    available_timings = available_times(booking_date, provider)
    busy_day_msg = None

    if len(available_timings) == 0:

        busy_day_msg = (
            "Ok, we are booked the rest of the day. "
            if booking_date
            else "I’m sorry we have no availabilities that day. "
        )

        busy_day_msg += "Please choose another day and time with A.M or P.M after time."

        options = build_date_options_str(provider.available_days)
        busy_day_msg = busy_day_msg + ' We have ' + options + ' available.'

    return busy_day_msg


def check_valid_date_time(booking_date, provider):
    """ Make sure the given datetime valid and not included in holidays """

    msg = None

    if not booking_date:
        msg = "Sorry I didn't understand that, what date works best for you?"

    elif booking_date and booking_date.isoweekday() not in provider.available_days:
        msg = "I'm sorry, our office is closed that day, please choose another day and say time with A.M or P.M after time."

    return msg


def check_date_time_available(booking_date, provider):
    """ Make sure the datetime is not already booked """

    dirty_msg = ''
    pre_msg = ''

    # 1. the time slot is filled but it is not a valid time
    if booking_date is None:
        dirty_msg = "Sorry I didn't understand that, what date and time works best for you?"

    # 2. the time is in between breaks. so deny that.
    elif check_breaks(booking_date, provider.breaks_set.all()):
        dirty_msg = "I'm sorry, our office is closed that day, Please choose another day and say time with A.M or P.M after time."

    elif available_times(booking_date, provider) and is_beyond_working_time_selected(booking_date, provider):
        dirty_msg = "I’m sorry, we are closed at that time, please choose another time that day."

    # check selected time is available
    if booking_date and not booking_date.strftime(TIME_FMT) in available_times(booking_date, provider):
        # if the time is not set because of user selected time is not available, then suggest next
        available_time = available_times(booking_date, provider)

        # Update : if user selected time is not available, then suggest next 2 available slots
        try:
            available_time_list = list(available_time)[:3]
        except IndexError:
            available_time_list = available_time

        if isinstance(available_time_list, list):
            try:
                times_available1 = available_time_list[0]
                times_available2 = available_time_list[1]
            except IndexError:
                times_available1 = available_time_list
                times_available2 = available_time_list

        if isinstance(available_time_list, OrderedDict):
            times_available1 = next(iter(available_time.keys()))
            times_available2 = next(iter(available_time.keys()))

        if len(available_time) == 1:
            dirty_msg = f"{times_available1}  is the only time available that day. Does that work for you?"
        elif len(available_time) == 0:
            dirty_msg = ""
        else:
            dirty_msg = f"Does {times_available1} work instead?"

        if times_available1 and times_available2 and is_below_working_time_selected(booking_date, provider):
            pre_msg = "I'm sorry, we are closed that time"

        elif is_below_working_time_selected(booking_date, provider):
            pre_msg = "I'm sorry, we are closed that time"

        elif is_beyond_working_time_selected(booking_date, provider):
            pre_msg = "I'm sorry, we are closed that time"

        else:
            pre_msg = "I'm sorry, that time is not available"

        return pre_msg + ". " + dirty_msg, times_available1

    # if dirty_msg:
    #         return dirty_msg, None

    return None, None


def get_appointment(user, account, provider):
    """ if appt already exist then fetch the details """
    from calendar_manager.models import CalendarDb

    try:
        appointment_obj = CalendarDb.objects.filter(
            users_customer=account, users_provider=provider).order_by('-id')[0]
    
    except CalendarDb.DoesNotExist:
        return JsonResponse({'user_exist': True, 'response_message': "I'm sorry. I can`t find your appointment from the phone number you texted in.\
        To book new appointment, just say day and time with A.M or P.M after time."})

    return appointment_obj


def get_user_account(user):
    """ Get user account """
    try:
        user_account = Account.objects.get(phone=user.user_id)
    except:
        user_account = None
    return user_account


def user_appointment_time(appt):
    """  # Month day at time"""
    return str(
        appt.start_time_local.strftime('%B %d at %I:%M %p')
    ) if appt else ''


def msg_for_reschedule_appt(appt, date):
    """ Retun existing appt """

    if appt.start_time_local < datetime.datetime.now():
        msg = "Hi{0} I’m sorry I  don’t see any upcoming appointments for you. \
        Please call us at this number to reschedule.".format(appt.first_name)

    elif not date:
        msg = (
            f"I see you have an appointment on {user_appointment_time(appt)}. "
            f"What day would you like to reschedule too? Just say day and time with A.M or P.M after time."
            if user_appointment_time(appt)
            else f"I'm sorry. I can`t find your appointment from the phone number you texted in. "
            f"To book new appointment, just say day and time with A.M or P.M after time."
        )
    else:
        msg = None

    return msg


def check_email_exist(email, comapany_id):
    return Account.registered_with_email_id(email, comapany_id)
