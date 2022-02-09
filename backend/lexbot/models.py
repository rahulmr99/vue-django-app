import datetime
import json
import logging
import pytz
from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from pynamodb import attributes
from pynamodb.models import Model

from backend.config import CONFIG

TESTS_IN_PROGRESS = getattr(settings, 'TESTS_IN_PROGRESS', False)


class ExpiringTableMixin:
    EXPIRE_TIME_MINS = 15
    expire_at = attributes.NumberAttribute()
    '''Table gets deleted after the expiry time'''

    def save(self, **kwargs):
        self.expire_at = (datetime.datetime.utcnow()
                          + datetime.timedelta(minutes=self.EXPIRE_TIME_MINS)
                          ).timestamp()
        return super().save(**kwargs)


class CallerInfoQueue(ExpiringTableMixin, Model):
    """
    when forwarding call from Twilio to AWS Connect
    we are not able to fetch both original and forwarding twilio number.
    In AWS Connect we were able to get the customer number. So here we are mapping customer number
    and company_id. This is a temporary table where the items must be cleaned after reaching Lex handler.
    """

    class Meta:
        table_name = f"{'test-' if TESTS_IN_PROGRESS else ''}twilio-caller-info-queue"
        read_capacity_units = 5
        write_capacity_units = 2
        host = CONFIG.DYNAMO_DB_HOST

    created_at = attributes.UTCDateTimeAttribute(default=datetime.datetime.utcnow)

    generalsettings_id = attributes.NumberAttribute()
    '''to keep track of provider that user has called to'''

    caller_number = attributes.UnicodeAttribute(hash_key=True, )
    provider_number = attributes.UnicodeAttribute(null=True, )
    caller_country = attributes.UnicodeAttribute(null=True, )
    user_choice = attributes.NumberAttribute(default=1)

    def __str__(self):
        return f'{self.caller_number}. Company ID: {self.generalsettings_id}'

    def has_choice(self, choice: int) -> bool:
        return self.user_choice == choice

    @property
    def want_booking(self) -> bool:
        return self.has_choice(1)

    @property
    def want_rescheduling(self):
        return self.has_choice(2)

    @property
    def want_cancelling(self):
        return self.has_choice(3)

    @property
    def want_help(self):
        return self.has_choice(4)

    @classmethod
    def save_from_request(cls, request, company_id):
        infoq = cls()
        infoq.caller_number = request.POST['From']
        infoq.provider_number = request.POST['To']

        # Get which digit the caller chose
        infoq.user_choice = int(request.POST['Digits'])

        infoq.caller_country = request.POST.get('FromCountry')
        infoq.generalsettings_id = int(company_id)
        infoq.save()
        return infoq

    @classmethod
    def get_caller_info(cls, customerNumber: str, delete=True) -> 'CallerInfoQueue':
        """return the instance but delete it from database."""
        try:
            callerinfo = CallerInfoQueue.query(customerNumber).next()
            logging.debug(f'Getting from Caller info saved {callerinfo}')
            if delete:
                callerinfo.delete()
            return callerinfo
        except StopIteration:
            raise Exception(f"CallerInfoQueue Not found for customer calling from {customerNumber}")


DEFAULT_MSG = 'Welcome to {company_name}! ' \
              'Press 1 to book an appointment,  ' \
              'press 2 to reschedule, ' \
              'press 3 to cancel, ' \
              'press 4 for all other questions.'


class VoiceBotConfig(TimeStampedModel):
    class Meta:
        ordering = ['-id', ]

    generalsettings = models.OneToOneField('app_settings.GeneralSettings', on_delete=models.CASCADE, )
    greeting_message = models.TextField(default=DEFAULT_MSG)
    use_audio = models.BooleanField(default=False, )
    greeting_voice = models.FileField(null=True, blank=True, )
    redirect_to_browser = models.BooleanField(default=True)
    redirect_telephone_number = models.CharField(blank=True, null=True, max_length=20, )

    def __str__(self):
        return f"Voice Bot Config of: {self.generalsettings}"

    def save(self, **kwargs):
        if '{company_name}' in self.greeting_message and self.generalsettings:
            self.greeting_message = self.greeting_message.format(company_name=self.generalsettings.company_name)
        super(VoiceBotConfig, self).save(**kwargs)


class LexSessionAttrsStore(ExpiringTableMixin, Model):
    """AWS Lex no longer provides session feature and this table is used to implement time based session"""

    class Meta:
        table_name = f"{'test-' if TESTS_IN_PROGRESS else ''}lex-session-store"
        host = CONFIG.DYNAMO_DB_HOST
        read_capacity_units = 5
        write_capacity_units = 2

    modified_at = attributes.UTCDateTimeAttribute()

    user_id = attributes.UnicodeAttribute(hash_key=True, )
    '''lex unique ID'''

    attrs = attributes.UnicodeAttribute(null=True)
    '''dict dumped and stored as str'''

    def save(self, **kwargs):
        self.modified_at = datetime.datetime.utcnow()
        return super().save(**kwargs)

    @classmethod
    def get(cls, user_id):
        try:
            return cls.query(user_id).next()
        except StopIteration:
            pass

    @classmethod
    def create(cls, user_id):
        c = cls()
        c.user_id = user_id
        c.save()
        return c

    @property
    def is_expired(self) -> bool:
        return (
                (self.modified_at - datetime.datetime.utcnow().astimezone(pytz.utc)).total_seconds()
                > (self.EXPIRE_TIME_MINS * 60))

    @property
    def session_attrs(self) -> dict:
        """return stored session attribute if available and not expired"""
        if self.attrs and not self.is_expired and self.attrs:
            return json.loads(self.attrs)
        return {}

    def store(self, attrs: dict):
        self.attrs = json.dumps(attrs)
        self.save()
