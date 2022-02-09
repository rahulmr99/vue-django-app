import logging
from django.utils import timezone
from django.utils.functional import cached_property
from typing import Union

from authentication_user.models import Account
from authentication_user.validators import validate_phone_number
from calendar_manager.models import CalendarDb
from lexbot.models import CallerInfoQueue
from .. import msgs

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class CurrentIntent(object):
    def __init__(self, intent_request: dict):
        self.slots: dict = intent_request['slots']
        self.confirmationStatus: str = intent_request.get('confirmationStatus')
        self.name: str = intent_request['name']
        self.slotDetails: dict = intent_request['slotDetails']

    def __str__(self):
        return f"{self.name}: {self.slots} with {self.confirmationStatus}"

    @property
    def has_confirmation(self):
        return self.confirmationStatus not in {None, 'None'}

    @property
    def is_confirmed(self):
        return self.confirmationStatus == 'Confirmed'

    @property
    def is_denied(self):
        return self.confirmationStatus == 'Denied'


class Bot(object):
    def __init__(self, intent_request: dict):
        self.alias: dict = intent_request['alias']
        self.version: str = intent_request['version']
        self.name: str = intent_request['name']


class AppointmentHandler(object):
    def __init__(self, company_id, providerPhoneNumber, callerPhoneNumber, callerCountry=None):
        """set required session attributes if not present"""
        self.company_id = company_id
        validate_phone_number(callerPhoneNumber)
        validate_phone_number(providerPhoneNumber)
        self.callerPhoneNumber = callerPhoneNumber
        self.providerPhoneNumber = providerPhoneNumber
        self.callerCountry = callerCountry

    @cached_property
    def provider(self) -> Account:
        provider: Account = Account.objects.filter(
            generalsettings_id=self.company_id, is_provider=True,
        ).prefetch_related('services').first()

        if not provider:
            """this should not happen"""
            raise Exception('At least there should be one provider account.')

        return provider

    @cached_property
    def customer_account(self) -> Union[Account, None]:
        """# get the customer account by phone number and return"""
        return Account.get_customer(
            phone=self.callerPhoneNumber, generalsettings_id=self.company_id, region_code=self.callerCountry,
        )

    @cached_property
    def calendar_appointment(self) -> Union[CalendarDb, None]:
        """# check whether user is having any appointments that is not expired"""
        # current_date_time = timezone.now().replace(tzinfo=pytz.timezone(self.customer_account.timezone))

        calendardb = CalendarDb.objects.filter(
            generalsettings_id=self.company_id,
            users_customer=self.customer_account,
            start_datetime__gt=timezone.now()
        ).first() if self.customer_account else None

        return calendardb if calendardb and calendardb.start_datetime else None

    @property
    def user_appointment_time(self) -> str:
        """  # Month day at time"""
        return str(
            self.calendar_appointment.start_time_local.strftime('%B %d at %I:%M %p')
        ) if self.calendar_appointment else ''

    def check_appointment_cancel_action(self) -> Union[str, None]:
        # case 1: there is no appointment
        if self.calendar_appointment is None:
            return msgs.APPOINTMENT_NOT_FOUND

        # case 2: if it can't be cancelled notify the user
        elif not self.calendar_appointment.is_cancelable:
            return msgs.CANCELLATION_POLICY_24

    @property
    def customer_name(self):
        return self.customer_account.name if self.customer_account else ''

    def get_customer_confirmation_for_cancel(self):
        # return msgs.CANCELLATION_CONFIRMATION.format(customer_name=self.customer_name,
        #                                              appointment_time=self.user_appointment_time)
        return msgs.CANCELLATION_CONFIRMATION

    def get_msg_intro(self):
        return (('Hi ' if self.customer_name else '')
                + str(self.customer_name)
                + ("!" if self.customer_name else ''))

    def get_msg_for_booking_date(self):
        hi_msg = self.get_msg_intro()
        msg = f"What day would you like to come in? Just say day and time with A.M or P.M after time."
        return hi_msg + (" " if hi_msg else '') + msg

    def get_msg_for_new_patient(self) -> str:
        return msgs.NEW_USER_QUEST

    def get_msg_for_reschedule_date(self):
        msg = (
            f"I see you have an appointment on {self.user_appointment_time}. "
            f"What day would you like to reschedule too? Just say day and time with A.M or P.M after time."
            if self.user_appointment_time
            else f"I'm sorry. I can`t find your appointment from the phone number you texted in. "
                 f"To book new appointment, just say day and time with A.M or P.M after time."
        )
        return f"{self.get_msg_intro()} {msg}"


class LexHandler(AppointmentHandler):
    """
        to help accessing the event keys with typed class attributes
    Notes
        sample event format is here
        https://docs.aws.amazon.com/lex/latest/dg/lambda-input-response-format.html#using-lambda-input-event-format
    """
    intents = set()
    '''intent names that can be handled by this'''

    @classmethod
    def handler(cls, event: dict, context: dict) -> dict:
        lexhandler = cls(event, context)
        lexhandler.check_current_intent()
        return lexhandler.run()

    def __init__(self, event: dict, context: dict):
        self.event = event
        self.conext = context
        self.intent = CurrentIntent(event['currentIntent'])
        self.slots = self.intent.slots
        self.bot = Bot(event['bot'])
        self.userId: str = event['userId']
        self.inputTranscript: str = event['inputTranscript']
        self.requestAttributes: dict = event.get('requestAttributes') or {}
        self.attrs: dict = event.get('sessionAttributes') or {}
        '''session attributes that will be persisted within session'''

        # if this is called from AWS connect, then it is not possible to have these attributes.
        # So get them from database stored by view
        if 'company_id' not in self.attrs and 'customerNumber' in self.attrs:
            callerinfo = CallerInfoQueue.get_caller_info(self.attrs['customerNumber'])
            self.attrs['callerCountry'] = callerinfo.caller_country
            self.attrs['callerPhoneNumber'] = callerinfo.caller_number
            self.attrs['providerPhoneNumber'] = callerinfo.provider_number
            self.attrs['company_id'] = callerinfo.generalsettings_id

        # init appointment handler
        super(LexHandler, self).__init__(
            self.attrs['company_id'],
            providerPhoneNumber=self.attrs['providerPhoneNumber'],
            callerPhoneNumber=self.attrs['callerPhoneNumber'],
            callerCountry=self.attrs.get('callerCountry'),
        )

    def check_current_intent(self):
        """sanity check for configured intent"""
        if self.intent.name not in self.intents:
            raise Exception('Intent with name ' + self.intent.name + ' not supported')

    def __str__(self):
        return str(self.__dict__)

    def run(self) -> dict:
        raise NotImplementedError
