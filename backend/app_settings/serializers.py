import requests
import json

from django.conf import settings

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from app_settings.models import TwilioAccount
from authentication_user.models import Account

from . import models


class WorkingPlanModelSerializer(ModelSerializer):
    show = serializers.SerializerMethodField('is_show', read_only=True)
    start = serializers.TimeField(
        format='%I:%M %p', input_formats=['%I:%M %p'], )
    end = serializers.TimeField(
        format='%I:%M %p', input_formats=['%I:%M %p'], )

    def is_show(self, obj):
        return False

    class Meta:
        model = models.WorkingPlan
        fields = [
            'id',
            'users',
            'enable',
            'show',
            'day',
            'start',
            'end'
        ]


class BusinessHourSerializer(serializers.Serializer):
    # full-calendar business hours to restrict view shown to the user
    # https://fullcalendar.io/docs/display/businessHours/
    dow = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6)
    )
    start = serializers.TimeField()
    end = serializers.TimeField()


class BreaksModelSerializer(ModelSerializer):
    show = serializers.SerializerMethodField('is_show', read_only=True)
    start = serializers.TimeField(
        format='%I:%M %p', input_formats=['%I:%M %p'], )
    end = serializers.TimeField(
        format='%I:%M %p', input_formats=['%I:%M %p'], )

    def is_show(self, obj):
        return False

    class Meta:
        model = models.Breaks
        fields = [
            'id',
            'users',
            'show',
            'day',
            'start',
            'end'
        ]


class GeneralSettingsModelSerializer(ModelSerializer):
    default_provider_id = serializers.SerializerMethodField(read_only=True)
    booked_fusion_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.GeneralSettings
        fields = [
            'id',
            'slug',
            'company_name',
            'company_email',
            'company_link',
            'google_analytics_id',
            'date_format',
            'send_notification',
            'captcha',
            'default_provider_id',
            'booked_fusion_number',
        ]

    def get_booked_fusion_number(self, obj):

        # If booked fusion number is not present, create it
        # Already exit update it if there any change
        is_twilio_account_exist = False
        try:
            booked_fusion_number = self.initial_data.get(
                'booked_fusion_number', None)
        except AttributeError:
            booked_fusion_number = None

        if booked_fusion_number:
            try:
                twilio_account = TwilioAccount.objects.get(
                    generalsettings=obj, sid__isnull=False)
                is_twilio_account_exist = True
            except TwilioAccount.DoesNotExist:
                twilio_account = None

            if not is_twilio_account_exist:
                twilio_account = TwilioAccount.objects.create(
                    generalsettings=obj, booked_fusion_number=booked_fusion_number)
            elif is_twilio_account_exist:
                old_number = twilio_account.booked_fusion_number
                twilio_account.booked_fusion_number = booked_fusion_number
                twilio_account.save()
                # When the bookedfusion number changes also notify the bot node server
                # So that it will serve from the new number instead the old no
                headers = {'Content-Type': 'application/json'}
                payload = {"number": str(booked_fusion_number),
                           "accountSid": str(twilio_account.account_sid),
                           "authToken": str(twilio_account.auth_token),
                           "serviceId": str(twilio_account.service_id),
                           "old_number": str(old_number)
                           }

                url = '{}/change'.format(settings.BOTKIT_SERVER_URL)
                requests.put(url, data=json.dumps(payload), headers=headers)
        else:
            twilio_account = TwilioAccount.objects.filter(
                generalsettings=obj, sid__isnull=False).only('booked_fusion_number').first()

        return twilio_account.booked_fusion_number if twilio_account is not None else None

    def get_default_provider_id(self, obj):
        return Account.objects.filter(generalsettings=obj, is_provider=True).values_list('pk', flat=True).first()


class InitialConfirmationModelSerializer(ModelSerializer):
    class Meta:
        model = models.InitialConfirmation
        fields = '__all__'


class CancellationSettingsModelSerializer(ModelSerializer):
    class Meta:
        model = models.CancellationSettings
        fields = '__all__'


class ReschedulingSettingsModelSerializer(ModelSerializer):
    class Meta:
        model = models.ReschedulingSettings
        fields = '__all__'


class ReminderModelSerializer(ModelSerializer):
    class Meta:
        model = models.Reminder
        fields = [
            'id',
            'users',
            'email_subject',
            'email_body',
            'send',
            'send_time',
            'send_type'
        ]
