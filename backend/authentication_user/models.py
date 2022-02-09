import datetime
import logging
import phonenumbers
import pytz
import uuid
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy
from django_extensions.db.fields import RandomCharField
from django_extensions.db.models import TimeStampedModel
from django_mysql.models import ListCharField
from itsdangerous import URLSafeTimedSerializer
from oauth2client.contrib.django_util.models import CredentialsField
from rest_framework.exceptions import PermissionDenied, ValidationError

from app_settings.models import WorkingPlan, Breaks, GeneralSettings
from authentication_user.validators import validate_phone_number
from mailer.utils import send_mail_from_template_str
from . import managers
from .choices import MAIL_STATUS

SIGNER = URLSafeTimedSerializer(settings.SECRET_KEY)

MAX_NUM_REMEMBERED = 20

TIME_ZONES = [(tz, tz) for tz in pytz.common_timezones if tz.startswith(
    'US') or tz in {'UTC'}] + [('EST', 'EST')]
'''time zones supported as of now'''


class Account(AbstractBaseUser, PermissionsMixin):
    class Meta:
        ordering = ['-id', '-created_at', '-name']
        unique_together = [
            # keep unique list of customers per account
            ('generalsettings', 'phone', 'country_code'),

            # keep unique list of customers per account.
            # The customers can register themselves under the email ID to different provider.
            ('generalsettings', 'email'),

            # keep unique list of customers per account.
            # The providers email ID must be unique across all the accounts.
            # ('email', 'password'),
            ('email', 'is_active'),
        ]

    generalsettings = models.ForeignKey(
        GeneralSettings, on_delete=models.CASCADE, )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date of creation")
    username = models.CharField(
        max_length=255, default='', blank=True, verbose_name='Username')

    email = models.EmailField(null=True, blank=True, verbose_name="Mail",
                              help_text='Used as unique ID/login ID for the account users/service providers')
    email1 = models.EmailField(null=True, blank=True)
    email2 = models.EmailField(null=True, blank=True)
    password = models.CharField(ugettext_lazy(
        'password'), max_length=128, null=True, blank=True)
    '''if this field is filled then email ID must be unique. only providers can login to the app'''

    name = models.CharField(max_length=50, verbose_name="Name")
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Last Name")

    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name="Mobile phone",
                             validators=[validate_phone_number])
    mobile = models.CharField(max_length=25, null=True, blank=True, verbose_name="Telephone",
                              validators=[validate_phone_number])
    '''country code must be stripped out before saving'''

    other_phones: list = ListCharField(
        base_field=models.CharField(max_length=20),
        max_length=MAX_NUM_REMEMBERED * 21,
        default=list,
    )
    '''list of last MAX_NUM_REMEMBERED phone numbers that the user called from to confirm another number. 
    saved with area code and country code.'''

    address = models.CharField(blank=True, null=True, max_length=255)
    state = models.CharField(blank=True, null=True, max_length=255)
    city = models.CharField(blank=True, null=True, max_length=255)
    country = models.CharField(blank=True, null=True, max_length=240)

    region_code = models.CharField(max_length=2, default='US')
    country_code = models.PositiveSmallIntegerField(default=1)
    '''if it is +1 then 1 will be saved'''

    zip_code = models.CharField(max_length=5, null=True, blank=True, )

    note = models.TextField(blank=True, null=True, verbose_name='User note')

    providers = models.ManyToManyField(
        'Account', blank=True, verbose_name='Providers list')
    services = models.ManyToManyField(
        'services.Service', blank=True, verbose_name='User services')

    receive_notification = models.BooleanField(default=True, blank=True)

    # if this is the root user the general_settings will be created
    # only one provider is going to be there for a company. so the below will be checked for all signing up account
    is_root_user = models.BooleanField(
        default=False, verbose_name="Root user ?")
    is_active = models.NullBooleanField(null=True, verbose_name="Active ?")
    is_admin = models.BooleanField(default=False, verbose_name="Admin ?")
    is_provider = models.BooleanField(default=False, verbose_name="Provider ?")
    is_secretarie = models.BooleanField(
        default=False, verbose_name="Secretarie ?")

    is_customers = models.BooleanField(
        default=False, verbose_name="Customers ?")
    '''the customers are the customer of the above account. They can't login to the app.'''

    is_staff = models.BooleanField(default=False)

    email_subscription_status = models.CharField(max_length=100, default=MAIL_STATUS.subscribed.name,
                                                 choices=MAIL_STATUS.choices(), editable=False, )
    '''if the user is subscribed then only he will receive mail notifications'''

    # this is provider specific setting may move to new model
    appointment_interval = models.DurationField(
        default=datetime.timedelta(minutes=10))
    '''time gap between appointment start times'''

    token = models.CharField(max_length=50, default='',
                             blank=True, null=True, verbose_name='Restore token')
    restore = models.BooleanField(default=False, verbose_name='Restore ?')

    timezone = models.CharField(
        default='EST', choices=TIME_ZONES, max_length=80, )
    '''it should be filled for Provider account only.'''

    chargebee_customer_id = models.CharField(
        max_length=25, null=True, blank=True)
    objects = managers.AccountManager()

    USERNAME_FIELD = 'email'

    def clean(self):
        if self.is_provider:
            if type(self).objects.filter(is_provider=True, generalsettings_id=self.generalsettings_id).count() > 2:
                raise ValidationError(
                    'is_provider', "There can't be more than one provider and one admin account.")

    def __str__(self):
        return f"{self.email} | {self.name}"

    @classmethod
    def registered_with_email_id(cls, email_id: str, company_id: str) -> bool:
        """check whether that the Email ID can be used to register new users"""
        q_email = models.Q(email=email_id)
        q_cid = models.Q(generalsettings_id=company_id)
        q_active = models.Q(is_active=True)
        q_is_cusomer = q_email & q_cid
        q_is_provider = q_email & q_active
        return cls.objects.filter(q_is_cusomer | q_is_provider).exists()

    def add_cusomer_number(self, number, commit=True):
        """save the number that user called from and not in the db"""
        if len(self.other_phones) > MAX_NUM_REMEMBERED:
            self.other_phones.pop(0)
        try:

            from lexbot.utils import parse_phone_number
            phone, country_code = parse_phone_number(number)
            # store the full number
            self.other_phones.append(f'{country_code}{phone}')
            if commit:
                self.save()
        except Exception as ex:
            logging.error(
                f"Failed to validate & save customer phone number {ex}")

    @property
    def has_subscribed(self):
        return self.email_subscription_status == MAIL_STATUS.subscribed.name

    @property
    def full_phone_number(self):
        """
        fully qualified phone number with country code prepended
        """
        return f'+{self.country_code}{self.phone}' if self.phone else None

    @classmethod
    def company_filter(cls, account, **kwargs):
        """
            return a queryset filtered for the generalsettings as same as the account
        Args:
            **kwargs (object): filter arguments
            account (Account): account to use for filtering generalsettings. mostly the request.user

        Returns:
            QuerySet:
        """
        return cls.objects.filter(generalsettings_id=account.generalsettings_id, **kwargs)

    @cached_property
    def enabled_google_api(self):
        return getattr(self, 'googlecredentials', None) is not None

    def has_same_company(self, account):
        return self.generalsettings_id == account.generalsettings_id

    def check_account_access(self, account):
        if not self.has_same_company(account):
            raise PermissionDenied

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return f"{self.name} {self.last_name or ''}"

    @classmethod
    def get_customer(cls,
                     generalsettings_id,
                     email=None,
                     phone: str = None,
                     country_code: str = None,
                     region_code: str = None):
        """Find and return customer account from email id or phone number"""
        qry = None
        customers = cls.objects.filter(
            generalsettings_id=generalsettings_id,
            is_customers=True,
        )
        if email:
            qry = models.Q(email=email)
        else:
            if isinstance(phone, (bytes, bytearray)):
                phone = phone.decode("utf-8")

            if (region_code and phone) or (phone is not None and '+' in phone):
                from lexbot.utils import parse_phone_number
                phone, country_code = parse_phone_number(
                    phone,  # mandatory
                    region=region_code,
                )

            if phone:
                # try to match without the country code
                qry = (models.Q(phone=phone) | models.Q(
                    other_phones__contains=phone))

                if country_code:
                    _full_number = f'{country_code}{phone}'
                    qry = (
                        qry
                        | (models.Q(phone=phone, country_code=country_code))
                        | models.Q(other_phones__contains=_full_number)
                    )

        if not qry:  # if both phone and email ID not given then return
            return

        try:
            return customers.filter(qry).get()
        except (Account.DoesNotExist, Account.MultipleObjectsReturned) as ex:
            logging.info(
                f'Failed with {ex} to user account for '
                f'{generalsettings_id} - {country_code} - {phone} - {email} - {region_code}'
            )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        new_account = False

        # set username if not already set
        if not self.username and self.email:
            self.username = self.email
        if not self.username and self.name:
            self.username = f'{self.name}-{uuid.uuid4()}'

        if not self.id and self.is_root_user:
            new_account = True
            # there will be only one provider for a company and that is the root user
            self.is_provider = True

            if not self.generalsettings_id:
                self.init_generalsettings_id()

        if not self.country_code and not self.phone:
            self.country_code = 1

        if self.is_provider and self.is_active is None:
            self.is_active = True

        if self.is_customers and self.is_active is not None:
            self.is_active = None

        # parse and save phone number
        if str(self.phone).startswith('+'):
            phonenumber = phonenumbers.parse(self.phone, None)
            self.phone = phonenumber.national_number
            self.country_code = phonenumber.country_code
            self.region_code = phonenumbers.region_code_for_country_code(
                phonenumber.country_code)

        if not self.email:  # serilizer sets empty string when email field is not filled
            self.email = None

        try:
            super(Account, self).save()
        except Exception as ex:
            logging.error(f"Failed to create account - {ex}")

        # create working plan items for that provider the first time
        if self.is_provider and new_account:
            self.create_default_working_pan()

    def create_default_working_pan(self):
        from services.models import Service

        WorkingPlan.init_for_user(self)
        Breaks.init_for_user(self)
        Service.create_default_services(self)

    def init_generalsettings_id(self, email=None):
        """
            create company specific settings per root user.
            Others from this company will be linked to this company using this settings model
        """
        if not self.generalsettings_id:
            # create other app settings
            generalsettings = GeneralSettings.create_app_settings(email)
            # link root user with company
            self.generalsettings_id = generalsettings.pk

    def send_mail(self, subject, context: dict, template: str, from_name=None, provider_email=None):

        if self.is_provider:
            subject = 'Your copy of ' + subject

        if provider_email:
            self.email = provider_email

        if self.email and self.has_subscribed:
            send_mail_from_template_str(
                subject, context, template, self.email, from_name)
        else:
            logging.error(
                f'Not sending {subject}. '
                'Because the mail ID is not filled or the customer has unsubscribed'
                f' {self.get_full_name()}. pk:{self.pk}'
            )

    def get_next_appoinment(self, provider):
        """
        Get upcoming appts
        """
        from calendar_manager.models import CalendarDb
        try:
            date = CalendarDb.objects.filter(users_customer=self).first()
            date = date.start_datetime if date else None
            if date and date.date() >= datetime.datetime.now().date():
                # convert the date time into provider's timezone
                if provider:
                    tzname = 'US/Eastern' if provider.timezone == 'EST' else provider.timezone
                    tz_obj = pytz.timezone(tzname)
                    appt_date = date.astimezone(tz_obj)
            else:
                return None
            return appt_date
        except CalendarDb.DoesNotExist:
            pass
        return None

    @cached_property
    def available_days(self) -> set:
        """
        self must be a provider. It returns the list of available days as per the WorkingPlan.
        It is ISO weekday set
        """
        return {wp.day for wp in self.workingplan_set.all() if wp.enable}


class ConfirmationCode(TimeStampedModel):
    """this model stores confirmation code with the signed key"""
    key = models.CharField(max_length=100)
    '''a key generated with the its dangerous library'''
    code = RandomCharField(unique=True, length=7, include_alpha=False,
                           include_punctuation=False, db_index=True)
    '''instead of sending the signed key to the user, send this code with which is easier to copy and read'''

    objects = models.Manager()

    @classmethod
    def validate_confirmation_code(cls, code, mail_id):
        """
            validate the confirmation code
        Args:
            code:
            mail_id:

        Returns:

        """
        confirmationcode = None
        try:
            confirmationcode = cls.objects.get(code=code)
            # check the age is less than 5 mins
            valid = SIGNER.loads(confirmationcode.key, max_age=300) == mail_id
        except Exception:
            valid = False
        finally:
            # remove the record from the database whether it is valid/invalid
            if confirmationcode:
                confirmationcode.delete()

        return valid

    @classmethod
    def generate_confirm_code(cls, mail_id):
        """
            inserts a record to db and returns code for the mail ID
        Args:
            mail_id (str): mail ID to be encoded

        Returns:
            str: confirmation code
        """
        confirmationcode = cls()
        confirmationcode.key = SIGNER.dumps(mail_id)
        confirmationcode.save()
        return confirmationcode.code


class GoogleCredentials(models.Model):
    """this model is used to store the google credentials for the user"""
    id = models.OneToOneField(
        Account, primary_key=True, parent_link=True, on_delete=models.CASCADE, )
    credential = CredentialsField()


class ProviderAccount(Account):
    """proxy model that is used for Authorizing providers only"""

    class Meta:
        proxy = True

    objects = managers.ProviderAccountManager()


class CustomerAccount(Account):
    """proxy model that is used for Authorizing providers only"""

    class Meta:
        proxy = True

    objects = managers.CustomerAccountManager()
