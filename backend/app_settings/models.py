import datetime

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.db.models import Min, Max
from django_extensions.db.fields import AutoSlugField
from django_ses.models import SESStat

from . import abstracts


class GeneralSettings(models.Model):
    slug = AutoSlugField(populate_from=['company_name', 'company_link', 'id'], unique=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    company_link = models.URLField(blank=True, null=True)
    google_analytics_id = models.CharField(max_length=255, blank=True, null=True)
    date_format = models.CharField(max_length=255, blank=True, null=True)
    send_notification = models.BooleanField(default=False)
    captcha = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return '[ GeneralSettings {} - {} : {}]'.format(self.company_name, self.company_email, self.company_link)

    class Meta:
        verbose_name = '1. GeneralSettings'
        ordering = ['-id', ]

    @classmethod
    def create_with_defaults(cls, email=None):
        return cls.objects.create(
            # company_name='My first company name',
            company_name='',
            # company_email='test@gmail.com',
            company_email=email if email else '',
            company_link='https://www.google.com',
            date_format='DMY',
        )

    def create_related_settings(self):
        from openvbx.models import VoiceMailConfig
        from lexbot.models import VoiceBotConfig
        for o2o_cls in [FeedbackConfig, InitialConfirmation, Reminder, CancellationSettings, ReschedulingSettings]:
            try:
                o2o_cls.create_for(self.pk)
            except IntegrityError:
                pass
        VoiceMailConfig.objects.get_or_create(generalsettings=self)
        VoiceBotConfig.objects.get_or_create(generalsettings=self)

    @classmethod
    def create_app_settings(cls, email=None):
        """
            create default app settings for a company
        Returns:
            GeneralSettings: instance created and associated with other settings
        """
        generalsettings = cls.create_with_defaults(email)
        generalsettings.create_related_settings()
        return generalsettings


class TwilioAccount(models.Model):
    generalsettings = models.ForeignKey(GeneralSettings, null=True, on_delete=models.CASCADE, )
    sid = models.CharField(max_length=250)
    account_sid = models.CharField(max_length=250, null=True, blank=True)
    auth_token = models.CharField(max_length=250, null=True, blank=True)
    service_id = models.CharField(max_length=250, null=True, blank=True)
    booked_fusion_number = models.CharField(max_length=25, null=True, blank=True, verbose_name="Booked Fusion Number")
    api_key = models.CharField(max_length=250, null=True, blank=True)
    api_key_secret = models.CharField(max_length=250, null=True, blank=True)
    ''' it will save the purchase number over Twilio'''


class InitialConfirmation(abstracts.AbstractEmailModel):
    users = models.ForeignKey('authentication_user.Account', blank=True, null=True, on_delete=models.PROTECT,
                              related_name="%(app_label)s_%(class)s_related", verbose_name='User')
    default_email_template_name = 'initial'
    default_email_subject = 'New Appointment: {type} ({first} {last}) on {time} with {provider}'

    class Meta:
        verbose_name = '4. InitialConfirmation'
        ordering = ['-id', ]

    def __str__(self):
        return '[ InitialConfirmation {} - {} : {}]'.format(self.users, self.email_subject, self.email_body)


class CancellationSettings(abstracts.AbstractEmailModel):
    default_email_template_name = 'cancellation'
    default_email_subject = 'Appointment Cancelled: {first} {last} on {time}'

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return f'<Cancellation Settings>: {self.email_subject}'


class ReschedulingSettings(abstracts.AbstractEmailModel):
    default_email_template_name = 'rescheduling'
    default_email_subject = 'Appointment Rescheduled: {first} {last} now on {time} (was {oldtime}) with {provider}'

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return f'<Reschedule Settings>: {self.email_subject}'


class Reminder(abstracts.AbstractEmailModel):
    TYPE_SEND = (
        (2, 'Client and Admin'),
        (1, 'Client'),
    )
    users = models.ForeignKey('authentication_user.Account', blank=True, null=True, verbose_name='User',
                              on_delete=models.CASCADE, )
    send = models.BooleanField(default=True)
    send_time = models.PositiveSmallIntegerField(default=24)
    send_type = models.PositiveSmallIntegerField(choices=TYPE_SEND, default=1)

    # defaults
    default_email_template_name = 'reminder'
    # default_email_subject = 'Appointment Reminder: {type} is on {time} ({provider})'
    default_email_subject = 'Appointment Reminder: Hi {first} your appointment is on {time} with {provider}'

    class Meta:
        verbose_name = '5. Reminder'
        ordering = ['-id', ]

    def __str__(self):
        return '[ Reminder {} {} - {}]'.format(self.generalsettings, self.users, self.email_subject)

    @property
    def is_send_to_provider(self):
        return self.send_type == 2


class FeedbackConfig(abstracts.AbstractEmailModel):
    send = models.BooleanField(default=True)
    send_time = models.FloatField(default=4, help_text='in hours')
    send_time_in_delta = models.DurationField(default=datetime.timedelta(hours=4), editable=False)
    google_rateus_link = models.URLField()
    yelp_rateus_link = models.URLField()

    objects = models.Manager()

    default_email_subject = "Review your recent experience"
    default_email_template_name = 'feedback'

    def __str__(self):
        return f'[ Feedback {self.send_time} - {self.send}]'

    class Meta:
        verbose_name = '6. Feedback mail settings'
        ordering = ['-id', ]

    def save(self, **kwargs):
        self.send_time_in_delta = datetime.timedelta(hours=self.send_time)
        super(FeedbackConfig, self).save(**kwargs)


class WorkingPlan(models.Model):
    TYPE_DAY = (  # iso weekday
        (7, 'Sunday'),
        (6, 'Saturday'),
        (5, 'Friday'),
        (4, 'Thursday'),
        (3, 'Wednesday'),
        (2, 'Tuesday'),
        (1, 'Monday'),
    )
    users = models.ForeignKey('authentication_user.Account', verbose_name='User', on_delete=models.CASCADE,
                              limit_choices_to={'is_provider': True})
    enable = models.BooleanField(default=True)
    day = models.PositiveSmallIntegerField(choices=TYPE_DAY, default=1, verbose_name='Day week')
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        verbose_name = '2. WorkingPlan'
        ordering = ['-id', ]

    def __str__(self):
        return '[ WorkingPlan {} - {} : {}]'.format(self.day, self.start, self.end)

    def clean(self):
        if self.end < self.start:
            raise ValidationError({'end': 'Invalid time'})

    @classmethod
    def init_for_user(cls, account):
        """create default working plan for the provider account. """
        cls.objects.bulk_create([
            cls(
                enable=(day_number != 7),  # Sunday is not enabled by default.
                users=account, day=day_number,
                start=datetime.time(9, 00),
                end=datetime.time(18, 00), ) for day_number in range(1, 8)
        ])

    @classmethod
    def get_business_hours(cls, account):
        """
            If the given user is provider then return his working plan in fullcalendar business hours format.
            Else calculatet the start/end based on all working plans of the company
        Args:
            account:

        Returns:
            list:
        """
        fltrs = dict(users=account) if account.is_provider else dict(
            users__generalsettings_id=account.generalsettings_id)
        qry = cls.objects.filter(**fltrs)
        business_hours = []

        # group by day
        for day, start, end in qry.values_list('day').order_by('day').annotate(Min('start'), Max('end')):
            business_hours.append(dict(
                dow=[0 if day == 7 else day],
                start=start,
                end=end,
            ))
        return business_hours


class Breaks(models.Model):
    TYPE_DAY = (
        (7, 'Sunday'),
        (6, 'Saturday'),
        (5, 'Friday'),
        (4, 'Thursday'),
        (3, 'Wednesday'),
        (2, 'Tuesday'),
        (1, 'Monday'),
    )
    users = models.ForeignKey('authentication_user.Account', verbose_name='User', on_delete=models.CASCADE,
                              limit_choices_to={'is_provider': True})
    day = models.PositiveSmallIntegerField(choices=TYPE_DAY, default=1, verbose_name='Day week')
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        verbose_name = '3. Breaks'
        ordering = ['-id', ]

    def __str__(self):
        return '[ Breaks {} - {} : {}]'.format(self.day, self.start, self.end)

    @classmethod
    def init_for_user(cls, account):
        for day_number in range(1, 6):
            cls.objects.create(
                users=account, day=day_number,
                start=datetime.time(12, 00),
                end=datetime.time(13, 00)
            )


class EmailDashboard(SESStat):
    class Meta:
        app_label = 'django_ses'
