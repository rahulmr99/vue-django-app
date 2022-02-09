import time
from collections import OrderedDict

import datetime
import logging
import os
import pytz
from django.utils.functional import cached_property
from raven_python_lambda import RavenLambdaWrapper
from typing import Dict

import lexbot.utils
from app_settings.models import WorkingPlan
from authentication_user.models import Account
from calendar_manager.models import CalendarDb
from calendar_manager.utils import check_breaks, filter_a_days_slots
from lexbot.handlers import utils
from lexbot.handlers.utils import filter_time_slots, build_date_options_str
from lexbot.helpers.request_mappers import LexHandler
from lexbot.helpers.response_mappers import *
from lexbot import msgs

REBOOK_INTENT = 'RescheduleAppointmentIntent'
BOOK_INTENT = 'SMSBot'

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
TIME_FMT = '%-I:%M %p'
TIME_ZONE = 'America/New_York'


class AppointmentSlotsMixin(LexHandler):
    def __init__(self, *args):
        super().__init__(*args)

        if self.intent.name == REBOOK_INTENT:
            self.attrs['rescheduleAppointment'] = str(1)

        # slots
        self.date: str = self.slots.get('Date')
        self.APTime: str = self.slots.get('APTime')
        self.Time: str = self.slots.get('Time')

        choice = self.slots.get('Choose')
        self.Choose: str = str(choice).lower() if choice else choice

        self.FirstName: str = (
                self.slots.get('FirstName') or (self.customer_account.name if self.customer_account else None)
        )
        self.EmailId: str = (
                self.slots.get('EmailId') or (self.customer_account.email if self.customer_account else None)
        )

        # the value will be 0 or 1
        returning_user = (
                (1 if self.customer_account else None)  # if customer account is there already set True
                or self.attrs.get('isReturningUser')  # set from AWS Connect functions
                or self.slots.get('ReturningUser')
        )
        self.ReturningUser: int = int(returning_user) if str(returning_user).isdigit() else None

        self.timezone = pytz.timezone(TIME_ZONE)

    @cached_property
    def customer_account(self):
        return Account.get_customer(
            self.company_id,
            email=self.slots.get("EmailId"),
            phone=self.callerPhoneNumber,
            country_code=self.callerCountry,
        )

    def get_slots(self):
        return {
            'Date': self.date,
            'APTime': self.APTime,
            'Time': self.Time,
            'Choose': self.Choose,
            'FirstName': self.FirstName,
            'ReturningUser': self.ReturningUser,
            'EmailId': self.EmailId,
        }

    def validate(self):
        """run all validations"""
        logging.debug('running validations')

        for validator_func in [
            # self.validate_aptime,
            self.validate_choice,
        ]:
            rslt = validator_func()
            if rslt:
                slot_name, message = rslt
                return elicit_slot(self.attrs, BOOK_INTENT, self.get_slots(), slot_name, message)

    def validate_choice(self):
        if self.Choose:
            if self.choice is None:
                self.Choose = None
                return (
                    'Choose', 'Would you like to repeat them or choose another day?'
                )

    @property
    def choice(self):  # analNSelect
        if self.Choose:
            if "repeat" in self.Choose:
                return 1
            if "choose" in self.Choose or "another" in self.Choose:
                return 2
        return None

    @property
    def to_elicit(self):
        return self.attrs.get('slotToElicit')

    @to_elicit.setter
    def to_elicit(self, slotName):
        self.attrs['slotToElicit'] = slotName

    def elicit_slot(self, slotName: str, message: str, response_card: dict = None):
        if message is not None:
            self.to_elicit = slotName
            return elicit_slot(self.attrs, BOOK_INTENT, self.get_slots(), slotName, message, response_card, )

    def confirm_intent(self, message: str, slotName: str = None, ):
        if slotName:
            self.to_elicit = slotName
        return confirm_intent(self.attrs, BOOK_INTENT, self.get_slots(), message)

    @property
    def parsed_date(self) -> Union[datetime.datetime, None]:
        return utils.parse_datetime(self.date)

    def parse_time(self, t: str) -> Union[datetime.datetime, None]:
        """the time could either be in 16:00 or 04:00 PM format"""
        if t is None or self.parsed_date is None or ':' not in t:
            return None
        return utils.parse_datetime(f'{self.date} {t}')

    @property
    def parsed_attr_time(self) -> Union[datetime.datetime, None]:
        """the time could either be in 16:00 or 04:00 PM format"""
        return self.parse_time(self.attrs.get('Time'))

    @property
    def parsed_datetime(self):
        return self.parse_time(self.Time)

    @property
    def repr_datetime(self):
        return self.parsed_datetime.strftime(TIME_FMT)

    @property
    def first_name(self):
        return self.FirstName.split(' ')[0].title()

    @property
    def last_name(self):
        return (self.FirstName.split(' ')[1] if ' ' in self.FirstName else '').title()

    @property
    def is_today(self):
        return self.parsed_date.date() == datetime.date.today()

    @property
    def is_rechedule(self) -> bool:
        return bool(int(self.attrs.get('rescheduleAppointment') or 0))

    @property
    def another_day_chosen(self):
        if self.to_elicit == 'Time':
            input_set = set(str(self.inputTranscript).lower().split())
            test_set = set(CHOOSE_ANOTHER_DAY.split())
            # 1. he opts for another day
            return bool(input_set.intersection(test_set))

    def fill_date_slot(self):
        # run validations
        msg = None
        if self.date:
            if self.parsed_date is None:
                self.date = None
                msg = "Sorry I didn't understand that, what date works best for you?"

            elif self.parsed_date and self.parsed_date.isoweekday() not in self.provider.available_days:
                self.date = None
                msg = "I'm sorry, our office is closed that day, " \
                      "please choose another day and say time with A.M or P.M after time."

        # clarification prompt
        elif self.to_elicit == 'Date':
            msg = (
                "Hmm, I'm having trouble understanding you, just say the day and "
                "time you would like to reschedule to. "
                "And say AM or PM next to time"
                if self.is_rechedule

                else "Hmm, I'm having trouble understanding you, try saying a specific day and time with am or pm. "
                     "Like Tuesday 8:30 am."
            )

        if not msg and not self.parsed_date:
            msg = (
                msgs.CHOOSE_ANOTHER_DAY if self.another_day_chosen
                else self.get_msg_for_reschedule_date() if self.is_rechedule
                else self.get_msg_for_booking_date()
            )

        if msg:
            return self.elicit_slot('Date', msg)


CHOOSE_ANOTHER_DAY = "choose another day"


class LexScheduleHandler(AppointmentSlotsMixin):
    intents = {REBOOK_INTENT, BOOK_INTENT}

    @cached_property
    def is_beyond_working_time_selected(self) -> bool:
        """when user tried to book out of the working hours"""
        return self.days_working_plan.end < self.slot_time_localized.time()

    @cached_property
    def is_below_working_time_selected(self) -> bool:
        """when user tried to book out of the working hours"""
        return self.parsed_datetime and self.days_working_plan.start > self.slot_time_localized.time()

    @property
    def parsed_date_localized(self) -> datetime.datetime:
        return self.timezone.localize(self.parsed_date)

    @property
    def slot_time_localized(self) -> datetime.datetime:
        """user selected time or just the date converted to time"""
        return self.timezone.localize(self.parsed_datetime or self.parsed_date)

    @cached_property
    def days_working_plan(self) -> WorkingPlan:
        return self.provider.workingplan_set.filter(day=self.parsed_date_localized.isoweekday()).get()

    @cached_property
    def available_times(self) -> Dict[str, datetime.datetime]:
        """return list of available slots for the given provider."""
        last_selected_time = self.parsed_attr_time or self.parsed_date
        last_selected_time = self.timezone.localize(last_selected_time)

        available_times = OrderedDict([
            (slot.strftime(TIME_FMT), slot)

            for slot in filter_a_days_slots(
                day=self.parsed_date_localized,
                providers_working_plan=self.days_working_plan,
                interval=self.provider.appointment_interval,
                providers_calendar_tasks=CalendarDb.objects.filter(users_provider=self.provider),
                providers_breaks=self.provider.breaks_set.all(),
            )

            # filter only latest slots than last selected time in the given date
            if (((slot > last_selected_time) and
                 # if the time is already filled, make sure that available time includes the selected slot time
                 slot >= self.slot_time_localized))
               or (last_selected_time == self.slot_time_localized and
                   slot == last_selected_time)
        ])
        return available_times

    def clear_datetime_slots(self):
        self.date = self.APTime = self.Time = None
        self.attrs.pop('Time', None)  # remove last remembered time

    def is_busy_day(self, build_options: bool = True):
        """return response to elicit if true. else return False"""
        logger.debug(f'check busy day: {self.date}, {self.parsed_date}, time: {self.Time}'
                     f'conf: {self.intent.confirmationStatus}, avail: {len(self.available_times)} '
                     f'inp: {self.inputTranscript}')

        if len(self.available_times) == 0:
            busy_day_msg = (
                "Ok, we are booked the rest of the day. "
                if self.parsed_attr_time
                else "I’m sorry we have no availabilities that day. "
            )
            self.clear_datetime_slots()

            busy_day_msg += "Please choose another day and time with A.M or P.M after time."

            if build_options:
                options = build_date_options_str(self.provider.available_days)
                busy_day_msg = busy_day_msg + ' We have ' + options + ' available.'

            return self.elicit_slot('Date', busy_day_msg)

    def save_appointment(self):
        """save appointments and trigger mails"""
        # create appointment inside lex itself
        # since we will not have access to slots once the request is fulfilled
        kwargs = {}
        if self.EmailId:
            kwargs['email'] = self.EmailId

        calendardb = CalendarDb.add_or_reschedule_appointment(
            start_time=self.parsed_datetime,
            provider=self.provider,
            customer=lexbot.utils.get_or_create_customer_account(
                self.customer_account,
                self.attrs.get('callerPhoneNumber'),
                self.provider.generalsettings_id,
                self.first_name,
                self.last_name,
                **kwargs
            ),
            service=(
                None
                if self.is_rechedule
                else lexbot.utils.get_service(self.provider, str(self.ReturningUser))
            ),
            appointment_id=(
                self.calendar_appointment.id
                if self.is_rechedule and self.calendar_appointment
                else None
            ),
        )

        self.get_new_user_email_id(calendardb)
        return close_fullfilled(
            self.attrs,
            msgs.THANKS_NOTE_AFTER_BOOK.format(
                time=self.repr_datetime,
                day=self.parsed_date.strftime("%A"),
                date=self.parsed_date.strftime("%d %b"),
            ),
            self.get_slots(),
        )

    def get_new_user_email_id(self, calendardb):
        """send sms asking new user's email address if it is voice bot"""
        if (not self.ReturningUser) and (not self.EmailId) and (self.attrs.get('botType') != 'SMS'):
            from openvbx.utils import send_sms
            provider_name = (calendardb.users_provider.name if calendardb.users_provider_id else None) or ''
            send_sms(
                to=self.callerPhoneNumber,
                from_number=self.providerPhoneNumber,
                body=msgs.GET_NEW_USER_MAIL_ID.format(
                    provider=provider_name,
                    time=self.repr_datetime,
                    day=self.parsed_date.strftime("%A"),
                    date=self.parsed_date.strftime("%d %b"),
                )
            )

    def fill_returning_user_slot(self):
        # validation after user input
        if self.ReturningUser is None and self.to_elicit == 'ReturningUser' and not self.intent.has_confirmation:
            return self.elicit_slot(
                'ReturningUser',
                "Hmm, I'm having trouble understanding you. Just say yes or no if you are a new patient",
            )

        # fill slot after confirmIntent
        if self.ReturningUser is None:
            if self.intent.has_confirmation:
                self.ReturningUser = 0 if self.intent.is_confirmed else 1
            else:
                return self.confirm_intent(self.get_msg_for_new_patient(), slotName='ReturningUser')

    def check_choose_another_day(self):
        if self.another_day_chosen:
            self.clear_datetime_slots()

    def fill_time_slot(self):
        """validate user input and fill time slot"""

        logger.debug(f'check time: {self.Time}, {self.parsed_attr_time}, '
                     f'conf: {self.intent.confirmationStatus}, '
                     f'inp: {self.inputTranscript}')

        # validate time slot filled
        if self.Time:
            dirty_msg = None
            # 1. the time slot is filled but it is not a valid time
            if self.parsed_datetime is None:
                dirty_msg = 'I did not recognize that, what time would you like to book your appointment?'
            # 2. the time is in between breaks. so deny that.
            elif check_breaks(self.parsed_datetime, self.provider.breaks_set.all()):
                dirty_msg = 'Our office is not open at that time, What time would you like to come in?'
            # 3. the time is beyond working hours
            elif self.available_times and self.is_beyond_working_time_selected:
                dirty_msg = "I’m sorry, we are closed at that time, please choose another time that day."

            if dirty_msg:
                self.Time = None
                return self.elicit_slot('Time', dirty_msg)

        elif self.to_elicit == 'Time':
            # the user is asked to input time
            # 1. the user is suggested with time and asked to input yes/no and lex doesn't understand the input
            if self.parsed_attr_time and not self.intent.has_confirmation:
                return self.elicit_slot(
                    'Time',
                    "I'm sorry, I didn’t understand you. If that time works for you just say yes, "
                    "if it doesn’t just say no.",
                )

            # 2. Lex doesn't understand user input for time
            elif not self.parsed_datetime and not self.intent.has_confirmation:
                return self.elicit_slot(
                    'Time',
                    'I did not recognize that, what time would you like to book your appointment?'
                )

        # check whether the user is setting suggested time
        if (not self.Time
                and self.parsed_attr_time
                and self.intent.has_confirmation):
            # if the user has accepted the suggested time then set it.
            if self.intent.is_confirmed:
                self.Time = self.parsed_attr_time.strftime('%H:%M')
                self.attrs.pop('Time')  # remove remembering time
            elif self.intent.is_denied:
                self.attrs['Time'] = next(iter(self.available_times.keys()))
                times_available = ", ".join(filter_time_slots(self.available_times))
                return self.elicit_slot(
                    'Time',
                    f'OK, please choose another time that day. We have {times_available} available. '
                    f'To {CHOOSE_ANOTHER_DAY} say just say "{CHOOSE_ANOTHER_DAY}".',
                )

        # check selected time is available
        elif self.Time and not self.parsed_datetime.strftime(TIME_FMT) in self.available_times:
            # if the time is not set because of user selected time is not available, then suggest next
            self.Time = None
            self.attrs['Time'] = next(iter(self.available_times.keys()))
            if len(self.available_times) == 1:
                msg = f"{self.attrs['Time']} is the only time available that day. Does that work for you?"
            else:
                msg = f"Does {self.attrs['Time']} work instead?"

            if self.available_times and self.is_below_working_time_selected:
                pre_msg = "I'm sorry, we are closed that time"
            else:
                pre_msg = "I'm sorry, that time is not available"

            return self.confirm_intent(f"{pre_msg}. {msg}", slotName="Time")

        # fill time slot with free choice
        if not self.parsed_datetime:
            if len(self.available_times) == 1:
                msg = f"{self.attrs['Time']} is the only time available that day. Does that work for you?"
                return self.confirm_intent(msg, slotName="Time")
            else:
                times_available = ", ".join(filter_time_slots(self.available_times))
                msg = (f"What time would you like to come that day? Please say A.M or P.M after time. "
                       f"We have {times_available} available.")
                return self.elicit_slot('Time', msg)

    def fill_name_slot(self):
        # validate name slot
        msg = (
            'Hmm, I’m having trouble understanding you. Just say your first and last name only.'
            if not self.FirstName and self.to_elicit == 'FirstName'

            else f"What's your first and last name?"
            if not self.FirstName

            else None
        )

        # get user's full name
        return self.elicit_slot('FirstName', msg, )

    def check_email_id_exists(self) -> bool:
        """check whether user can register with the email ID"""
        return (self.EmailId and self.company_id
                and Account.registered_with_email_id(self.EmailId, self.company_id))

    def fill_email_slot(self):
        if not self.EmailId:
            # validate name slot
            msg = (
                'Hmm, I’m having trouble understanding you. Just type in your E-mail ID'
                if not self.EmailId and self.to_elicit == 'EmailId'

                else "Please provide another E-mail ID. This is already registered with us."
                if self.check_email_id_exists()

                else f'Thanks and last step. '
                f'Please reply back with just your primary email address. '
                f'We may send email reminders and communicate with you by email.'
                if not self.EmailId and self.attrs.get('botType') == 'SMS'

                else None
            )

            # get user's full name
            if msg:
                return self.elicit_slot('EmailId', msg, )

    def run(self):
        # todo: update this to be the timezone selected for the given provider
        os.environ['TZ'] = TIME_ZONE
        time.tzset()
        logger.debug(f'time: {self.Time}, attrTime: {self.attrs}')
        # validate and fill slots in order
        for _func in [
            self.validate,
            self.fill_returning_user_slot,
            self.check_choose_another_day,
            self.fill_date_slot,
            self.is_busy_day,
            self.fill_time_slot,
            self.fill_name_slot,
            self.fill_email_slot,
        ]:
            rslt = _func()
            if rslt:
                return rslt

        # got the customer info already so move to saving appointment
        return self.save_appointment()


@RavenLambdaWrapper()
def handler(event, context):
    return LexScheduleHandler.handler(event, context)
