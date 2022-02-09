import pytz
import uuid
from datetime import timedelta, datetime

import vobject
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.functional import cached_property
from django_extensions.db.models import TimeStampedModel
from django_mysql.models import QuerySetMixin, ListCharField
from typing import Union

from rest_framework.exceptions import ValidationError

from openvbx.utils import send_sms, send_telegram
from app_settings.abstracts import AbstractEmailModel
from app_settings.models import GeneralSettings
from app_settings.models import (Reminder, InitialConfirmation, ReschedulingSettings, CancellationSettings,
                                 FeedbackConfig, TwilioAccount)
from app_settings.utils import reverse_fullurl
from authentication_user.models import SIGNER
from lexbot.handlers.utils import parse_datetime
from calendar_manager.utils import convert_dt_to_provider_timezone

__all__ = ['CalendarDb']


def format_for_google_calendar(time: datetime):
    # return time.strftime('%Y%m%dT%I%M00Z')
    return time.strftime('%Y%m%dT%H%M%S')


EMAIL_TIME_FMT = "%A, %B %d, %Y at %-I:%M %p"
ICAL_URL_NAME = 'api_v1:calendardb-add-to-ical-outlook'

CalendarDbQuerySetType = Union['CalendarDbQuerySet', models.QuerySet, ]
'''useful for type annotating'''

SALT = 'calendar-db-signer-salt'


class CalendarDbQuerySet(QuerySetMixin, models.QuerySet):
    def active_appointments(self) -> CalendarDbQuerySetType:
        """return appointments that are not cancelled"""
        return self.filter(is_unavailable=False)

    def has_reminders(self) -> CalendarDbQuerySetType:
        return self.active_appointments().filter(
            remember=False,  # exclude appoints that already sent reminder for
            # based on the Reminder setting filter out which are set to False
            users_provider__generalsettings__reminder__send=True,
        )

    def annotate_feedback_send_time(self) -> CalendarDbQuerySetType:
        feedback_send_time_expr = models.ExpressionWrapper(
            models.F('start_datetime') + models.F(
                'users_provider__generalsettings__feedbackconfig__send_time_in_delta'),
            output_field=models.DateTimeField()
        )
        return self.annotate(
            feedback_send_time=feedback_send_time_expr
        )

    def waiting_for_feedback(self) -> CalendarDbQuerySetType:
        return self.active_appointments().annotate_feedback_send_time().filter(
            users_provider__generalsettings__feedbackconfig__send=True,
            sent_feedback_mail=False,  # exclude appoints that already got feedback for
            feedback_send_time__lte=timezone.now()
        )

    def is_overlapping(self, start_time: datetime, end_time: datetime = None, tzname=None, converted_tz=False) -> bool:
        # convert datetime to UTC since db will have time stored in UTC only
        
        # start_time = start_time.astimezone(pytz.utc)

        # start_time = start_time.replace(
        #     tzinfo=None).astimezone(provider_timezone)
        # start_time = start_time.astimezone(pytz.utc)

        if tzname and not converted_tz:
            tz_obj = pytz.timezone(tzname)
            timezone.activate(tz_obj)
            start_time = start_time.astimezone(pytz.utc)
            end_time = end_time.astimezone(pytz.utc)

        filters = models.Q(
            start_datetime__lte=start_time,
            end_datetime__gte=start_time,
        )
        if end_time:
            # end_time = end_time.astimezone(pytz.utc)
            filters = (
                models.Q(start_datetime__gt=start_time,
                         start_datetime__lt=end_time, )
                | models.Q(end_datetime__gt=start_time, end_datetime__lt=end_time, )
                | models.Q(start_datetime__lt=start_time, end_datetime__gt=end_time)
            )
        return self.filter(filters).exists()

class CalendarDb(TimeStampedModel):
    TYPE_STATUS = (
        ('very_bad', 'very bad'),
        ('bad', 'bad'),
        ('normal', 'normal'),
        ('good', 'good'),
        ('very_good', 'very good'),
    )
    book_datetime = models.DateTimeField(auto_now_add=True)
    generalsettings = models.ForeignKey(
        'app_settings.GeneralSettings', editable=False, on_delete=models.CASCADE, )
    users_provider = models.ForeignKey('authentication_user.Account', related_name='User provider+', blank=True,
                                       null=True, verbose_name='User provider', on_delete=models.SET_NULL, )
    users_customer = models.ForeignKey('authentication_user.Account', related_name='User customer+', blank=True,
                                       null=True, on_delete=models.SET_NULL, )
    services = models.ForeignKey(
        'services.Service', blank=True, null=True, on_delete=models.CASCADE, )
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    is_unavailable = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    uid = models.CharField(max_length=100, blank=True, default=uuid.uuid4)
    remember = models.BooleanField(default=False)
    sent_feedback_mail = models.BooleanField(default=False, editable=False, )
    rate = models.CharField(
        max_length=30, choices=TYPE_STATUS, default='normal')
    comment = models.TextField(blank=True, null=True)
    google_calendar_event_link = models.URLField(blank=True, null=True, )
    google_calendar_event_id = models.CharField(
        max_length=80, db_index=True, null=True)

    old_start_times: list = ListCharField(
        base_field=models.CharField(max_length=40),
        max_length=10 * 41,
        default=list,
    )
    '''keep last 10 start times if the appointment is rescheduled'''

    objects = CalendarDbQuerySet.as_manager()

    def save(self, **kwargs):
        if not self.generalsettings_id:
            if self.users_provider_id and self.users_provider.generalsettings_id:
                self.generalsettings_id = self.users_provider.generalsettings_id
            elif self.users_customer_id and self.users_customer.generalsettings_id:
                self.generalsettings_id = self.users_customer.generalsettings_id
        super(CalendarDb, self).save(**kwargs)

    def has_overlapping_appointments(self, start_time, end_time,tzname=None) -> bool:
        """return True of any of appointment overlaps"""
        qs = type(self).objects.filter(
            users_provider_id=self.users_provider_id)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        return qs.is_overlapping(start_time, end_time, tzname)

    def set_times(self, start_time, end_time=None, service=None, tzname=None, rasa_bot=None):
        """convert time to the provider's timezone and check for any overlap"""
        
        from services.models import Service
        service = service or self.services
        end_time = (
            end_time if end_time
            else (start_time + timedelta(minutes=service.duration)) if service
            else (start_time + timedelta(minutes=Service.DEFAULT_DURATION))
        )

        tzname = 'US/Eastern' if tzname == "EST" else tzname

        if tzname:
            tz_obj = pytz.timezone(tzname)
            timezone.activate(tz_obj)
            _start_time = timezone.make_aware(start_time, tz_obj)
            _end_time = timezone.make_aware(end_time, tz_obj)

            # existing appointment
            if self.has_overlapping_appointments(_start_time, _end_time, tzname):
                if rasa_bot:
                    return False
                raise ValidationError({"error": "Slot is already booked"})
        else:
            _start_time = start_time
            _end_time = end_time

        self.start_datetime = _start_time
        self.end_datetime = _end_time
        
        return True

    def get_encoded_token(self):
        """return a token that is safe to be sent in the external links"""
        return SIGNER.dumps(self.pk, salt=SALT)

    @classmethod
    def add_or_reschedule_appointment(
            cls, provider, customer, start_time: datetime, service=None, end_time: datetime = None, note: str = '',
            appointment_id=None, rasa_bot=None, is_import_appt=None
    ) -> 'CalendarDb':
        from . import tasks
        calendardb = get_object_or_404(
            CalendarDb, id=appointment_id) if appointment_id else cls()

        calendardb.users_provider = provider
        calendardb.users_customer = customer
        if service:
            calendardb.services = service

        if note:
            calendardb.notes = note

        if appointment_id:  # reset sending reminders
            calendardb.remember = False
            # save last 10 old times
            if len(calendardb.old_start_times) > 9:
                calendardb.old_start_times.pop(0)
            calendardb.old_start_times.append(str(calendardb.start_datetime))

        tzname = provider.timezone
        set_times = calendardb.set_times(
            start_time, end_time, service, tzname, rasa_bot)

        if not set_times and rasa_bot:
            return False
        
        calendardb.save()
        timezone.deactivate()

        # send emails and update google calendar
        if appointment_id:
            tasks.async_run_calendar_func(
                calendardb.pk, 'send_rescheduled_email')

            # Added tzname 3 arg for convert the date time to corresponding providers timezone
            tasks.add_to_google_calendar_task(calendardb.pk, reschedule=True, tzname=tzname)
        else:
            if not is_import_appt:
                tasks.async_run_calendar_func(calendardb.pk, 'send_initial_email')
                # Added tzname 3 arg for convert the date time to corresponding providers timezone
                tasks.add_to_google_calendar_task(calendardb.pk, tzname=tzname)

        return calendardb

    def cancel_appointment(self):
        self.is_unavailable = True
        self.save()
        # send emails and remove google calendar events
        from . import tasks
        tasks.async_run_calendar_func(self.pk, 'send_cancellation_email')
        tasks.add_to_google_calendar_task(calendar_pk=self.pk, remove=True)

    def get_google_calendar_link(self, customer=False):

        # Each provider have different timezone so when adding booking date time to gcalndar
        # Make sure date time is converted to providers timezone
        
        if self.users_provider.timezone:
            tzname = 'US/Eastern' if self.users_provider.timezone and self.users_provider.timezone == 'EST' else self.users_provider.timezone
            tzname = pytz.timezone(tzname)
            # start_time = tzname.normalize(self.start_datetime.astimezone(tzname))
            # end_time = tzname.normalize(self.end_datetime.astimezone(tzname))
            start_time = self.start_datetime.astimezone(tzname)
            end_time = self.end_datetime.astimezone(tzname)

        if customer:
            tzname = 'US/Eastern' if self.users_provider.timezone and self.users_provider.timezone == 'EST' else self.users_provider.timezone
            tzname = pytz.timezone(tzname)
            start_time = self.start_datetime.astimezone(tzname)
            end_time = self.end_datetime.astimezone(tzname)

        else:
            start_time = self.start_time_local
            end_time = self.end_time_local


        params = {
            'action': 'TEMPLATE',
            'text': f'Appointment Reminder: {self.service_name}',
            'dates': f"{format_for_google_calendar(start_time)}/{format_for_google_calendar(end_time)}",
            'location': '',
            'details': f'Appointment Reminder: {self.service_name}',
            'sf': 'true'
        }

        # todo: the details should have links to change/view the appointment like below
        # View%2FChange+Appointment%3A%0Ahttps%3A%2F%2Fapp.acuityscheduling.com%2Fschedule.php%3Fowner%3D13600687%26id%5B%5D%3D36665bf893cea621eac0dbed5e5b9705%26action%3Dappt%0A%0A%28created+by+Acuity+Scheduling%29%0AAcuityID%3D113096529%0AGoogle

        import urllib.parse
        params = urllib.parse.urlencode(params)
        return f"https://www.google.com/calendar/render?{params}&amp;output=xml"

    @property
    def service_name(self):
        return self.services.name if self.services_id else ''

    @property
    def last_scheduled_time(self) -> str:
        """if the appoinment is rescheduled fetch the last stored time and localise the time from UTC"""
        time = self.get_localtime(
            self.old_start_times[-1]) if self.old_start_times else None
        return time.strftime(EMAIL_TIME_FMT) if time else ''

    def get_email_context(self, customer=False):
        type = self.service_name
        first = (self.users_customer.name if self.users_customer_id else None) or ''
        last = (self.users_customer.last_name if self.users_customer_id else None) or ''

        # convert time to providers timezone
        appt_dt = convert_dt_to_provider_timezone(self)
        time = appt_dt.strftime(EMAIL_TIME_FMT)
        duration = self.services.duration if self.services_id else None

        calendar = 'BookedFusion Appointment'
        '''google calendar schedule title'''

        # googlehref = self.get_google_calendar_link()
        googlehref = self.get_google_calendar_link(customer)
        provider = self.users_provider.get_full_name()
        service_name = self.service_name

        # fixme: check and update cancel link
        viewhref = f'{reverse_fullurl()}/#/cancel/{self.uid}'
        '''link to cancel appointment'''

        exporthref = reverse_fullurl(ICAL_URL_NAME, pk=self.id, json=True)
        '''link to download icalendar file'''

        oldtime = self.last_scheduled_time

        location = ''
        '''not implemented and used in cancellation template'''

        # for getting feedback from user
        token = self.get_encoded_token()
        feedback_links = {}
        for rating in range(1, 6):
            feedback_links[rating] = reverse_fullurl(
                'feedback:get-feedback', token, rating)

        return locals()

    # @property
    # def is_cancelable(self):
    #     """can be cancelled only one day before"""

    #     return (self.start_datetime - timezone.now()) > timedelta(hours=24)

    # checking the appt is cancelable by converting the date time to providers timezone
    def is_cancelable(self, provider):
        """can be cancelled only one day before"""
        tzname = pytz.timezone(provider.timezone)
        timezone_time = self.start_datetime.replace(
            tzinfo=None).astimezone(tzname)
        timezone_now = datetime.now().replace(tzinfo=None).astimezone(tzname)
        return (timezone_time - timezone_now) > timedelta(hours=24)

    @staticmethod
    def get_localtime(dt: Union[datetime, str]) -> Union[datetime, None]:
        """the database has time stored in UTC. We need to convert it before using showing back to users"""
        dt = parse_datetime(dt) if type(dt) == str else dt
        return timezone.localtime(dt) if dt else None

    @property
    def start_time_local(self):
        return self.get_localtime(self.start_datetime)

    @property
    def end_time_local(self):
        return self.get_localtime(self.end_datetime)

    @cached_property
    def reminder_setting(self) -> Reminder:
        reminder, _ = Reminder.objects.get_or_create(
            generalsettings_id=self.generalsettings_id)
        return reminder

    @cached_property
    def initialconfirmation_setting(self) -> InitialConfirmation:
        initial, _ = InitialConfirmation.objects.get_or_create(
            generalsettings_id=self.generalsettings_id)
        return initial

    @cached_property
    def feedback_setting(self) -> FeedbackConfig:
        fc, _ = FeedbackConfig.objects.get_or_create(
            generalsettings_id=self.generalsettings_id)
        return fc

    @cached_property
    def rescheduling_setting(self) -> ReschedulingSettings:
        resch, _ = ReschedulingSettings.objects.get_or_create(
            generalsettings_id=self.generalsettings_id)
        return resch

    @cached_property
    def cancellation_setting(self) -> CancellationSettings:
        cancell, _ = CancellationSettings.objects.get_or_create(
            generalsettings_id=self.generalsettings_id)
        return cancell

    @cached_property
    def make_vobject(self) -> object:
        cal = vobject.iCalendar()
        cal.add('vevent')
        if self.uid:
            cal.vevent.add('UID').value = self.uid
        cal.vevent.add('DTSTAMP').value = self.book_datetime

        summary = "Appointment: {type} ({first} {last}) on {time} with {provider}".format(
            **self.get_email_context())
        cal.vevent.add('DESCRIPTION').value = self.notes or summary
        cal.vevent.add('SUMMARY').value = summary
        
        # Each provider have different timezone so when adding booking date time to gcalndar
        # Make sure date time is converted to providers timezone
        if self.users_provider.timezone:
            provider_timezone = pytz.timezone(self.users_provider.timezone)
            cal.vevent.add('DTSTART').value = provider_timezone.localize(self.start_datetime.replace(tzinfo=None))
            cal.vevent.add('DTEND').value = provider_timezone.localize(self.end_datetime.replace(tzinfo=None))
        else:
            if self.start_datetime:
                cal.vevent.add('DTSTART').value = self.start_time_local
            if self.end_datetime:
                cal.vevent.add('DTEND').value = self.end_time_local

        return cal.serialize()

    def send_email(self, emailsetting: AbstractEmailModel, send_to_provider=False):
        try:
            generalsettings_obj = GeneralSettings.objects.get(id=emailsetting.generalsettings.id)
        except GeneralSettings.DoesNotExit:
            generalsettings_obj  = None
        
        if generalsettings_obj:
            company_name = generalsettings_obj.company_name
            company_email = generalsettings_obj.company_email
        else:
            company_name = "BookedFusion"
            company_email = None
        
        # kwargs = dict(subject=emailsetting.email_subject.format(**self.get_email_context()),
        #               context=self.get_email_context(),
        #               template=emailsetting.email_body, 
        #               from_name=company_name,)

        if self.users_customer_id:
            
            # kwargs = dict(subject=emailsetting.email_subject.format(**self.get_email_context()),
            #           context=self.get_email_context(),
            #           template=emailsetting.email_body, 
            #           from_name=company_name,
            #           )
            kwargs = dict(subject=emailsetting.email_subject.format(**self.get_email_context(customer=True)),
                      context=self.get_email_context(customer=True),
                      template=emailsetting.email_body,
                      from_name=company_name)
            
            self.users_customer.send_mail(**kwargs)

        # send all emails to providers company email instead their primary email
        if send_to_provider and self.users_provider_id:
            kwargs = dict(subject=emailsetting.email_subject.format(**self.get_email_context()),
                      context=self.get_email_context(),
                      template=emailsetting.email_body,
                      from_name=company_name,
                      provider_email=company_email if company_email else None)

            self.users_provider.send_mail(**kwargs)

    def send_initial_email(self):
        self.send_email(self.initialconfirmation_setting,
                        send_to_provider=True)

    def send_rescheduled_email(self):
        self.send_email(self.rescheduling_setting, send_to_provider=True)

    def send_cancellation_email(self):
        self.send_email(self.cancellation_setting, send_to_provider=True)

    def send_reminder_email(self):
        self.send_email(self.reminder_setting,
                        self.reminder_setting.is_send_to_provider)

    def send_feedback_email(self):
        self.send_email(self.feedback_setting, )

    def send_sms_reminder(self):
        if self.users_customer_id and self.users_customer.full_phone_number:
            temp_subject = self.reminder_setting.email_subject.format(
                **self.get_email_context())
            try:
                twilio_account = TwilioAccount.objects.get(
                    generalsettings=self.generalsettings)
            except TwilioAccount.DoesNotExit:
                twilio_account = None

            from_no = twilio_account.booked_fusion_number if twilio_account else None
            # temp_subject += ".\n To opt out, reply 'STOP'."
            # todo: fill the number of provider in to the from field
            send_sms(self.users_customer.full_phone_number,
                     temp_subject, from_no)

    def send_reminders(self, force_send=False):
        if self.remember and not force_send:
            return
        reminder_interval = timedelta(
            hours=self.users_provider.generalsettings.reminder.send_time)
        send_time: datetime = timezone.now() + reminder_interval

        # send reminder only when it is booked prior to send time
        # todo: convert this to queryset function and filter the records when querying itself
        if ((self.start_datetime - self.book_datetime) >= reminder_interval) and self.start_datetime < send_time:
            # update attribute
            self.remember = True
            self.save()

            if self.users_customer_id:
                send_telegram(
                    f'send email to: {self.users_customer.email}\n send sms to: {self.users_customer.full_phone_number}\n'
                )
            self.send_reminder_email()
            self.send_sms_reminder()

    def __str__(self):
        return f'[ CalendarDb {self.book_datetime} {self.users_provider} - {self.is_unavailable}]'

    class Meta:
        verbose_name = '1. Calendar'
        ordering = ['-id', '-book_datetime']
