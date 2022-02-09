import uuid
import pytz
from datetime import datetime
import dateutil.parser

from django.db import models
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from authentication_user.models import Account
from authentication_user.serializers import AccountModelSerializer
from calendar_manager.fields import TzDateTimeField
from services.models import Service
from services.serializers import ServiceModelSerializer
from calendar_manager.utils import convert_dt_to_provider_timezone
from .models import *


class CalendarDbModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarDb
        fields = [
            'id',
            'book_datetime',
            'users_provider',
            'users_customer',
            'services',
            'start_datetime',
            'end_datetime',
            'is_unavailable',
            'notes',
        ]


class CalendarDbFullModelSerializer(serializers.ModelSerializer):
    services = ServiceModelSerializer()

    class Meta:
        model = CalendarDb
        fields = [
            'id',
            'book_datetime',
            'users_provider',
            'users_customer',
            'services',
            'start_datetime',
            'end_datetime',
            'is_unavailable',
            'notes',
        ]


SERIALIZER_FIELD_MAPPING = serializers.ModelSerializer.serializer_field_mapping.copy()
SERIALIZER_FIELD_MAPPING.update({
    models.DateTimeField: TzDateTimeField
})


class CalendarDbMainFullModelSerializer(serializers.ModelSerializer):
    users_customer = AccountModelSerializer()
    title = serializers.SerializerMethodField('is_title', read_only=True)
    start = serializers.SerializerMethodField('is_start', read_only=True)
    end = serializers.SerializerMethodField('is_end', read_only=True)

    serializer_field_mapping = SERIALIZER_FIELD_MAPPING

    def is_title(self, obj: CalendarDb):
        return f'{obj.services.name if obj.services_id else ""}: ' \
               f'{obj.users_customer.name if obj.users_customer_id else ""}'

    def is_start(self, obj):
        return convert_dt_to_provider_timezone(obj)

    def is_end(self, obj):
        return convert_dt_to_provider_timezone(obj, True)

    class Meta:
        model = CalendarDb
        fields = [
            'id',
            'book_datetime',
            'title',
            'start',
            'end',
            'users_provider',
            'users_customer',
            'services',
            'start_datetime',
            'end_datetime',
            'is_unavailable',
            'notes',
        ]


class FreeDaySerializer(serializers.Serializer):
    page = serializers.IntegerField()
    service_id = serializers.IntegerField()
    provider_id = serializers.IntegerField()
    daydate = serializers.DateTimeField(required=False)


class ResponseItemDateSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    date = serializers.DateTimeField(format='%A, %B %d, %Y')
    time = serializers.DateTimeField(format='%-I:%M%P')
    choice = serializers.BooleanField(default=False)
    block = serializers.BooleanField(default=False)
    cancel = serializers.BooleanField(default=False)
    key = serializers.CharField()

    def to_representation(self, instance):
        tzname = self.context.get("tzname")

        datetime_aware = instance['time'].astimezone(pytz.timezone(tzname))
        data = super(ResponseItemDateSerializer,
                     self).to_representation(instance)
        data.update({'time': datetime_aware.strftime("%I:%M %p")})
        return data


class ResponseItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    number = serializers.CharField()
    caption = serializers.CharField(allow_blank=True)
    choice = serializers.BooleanField()
    date = serializers.ListSerializer(child=ResponseItemDateSerializer())


class ResponseListSerializer(serializers.Serializer):
    days = serializers.ListSerializer(child=ResponseItemSerializer())


class CancelSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    uid = serializers.CharField(required=False)

    def validate(self, attrs):
        id = attrs.get('id', None)
        uid = attrs.get('uid', None)
        if not id and not uid:
            raise serializers.ValidationError('Parameters not exist.')
        if uid:
            calendar_obj = CalendarDb.objects.filter(
                uid=uid).active_appointments()
            if not calendar_obj.exists():
                raise serializers.ValidationError('Uid not exist.')
        return attrs


class IcalOutlookSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        id = attrs.get('id', None)
        calendar_obj = CalendarDb.objects.filter(
            id=id,
        )
        if not calendar_obj.exists():
            raise serializers.ValidationError('Appointment not exist.')
        attrs['calendar_obj'] = calendar_obj.first()
        return attrs


class RecurringAddDateMassSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    service = serializers.IntegerField()
    type = serializers.CharField()
    count = serializers.IntegerField()


class RecurringResponseDateSerializer(serializers.Serializer):
    date = serializers.ListSerializer(child=ResponseItemDateSerializer())


class FilterAppointmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        id = attrs.get('id', None)
        calendar_obj = CalendarDb.objects.filter(
            users_customer=id,
            # start_datetime__gte=timezone.now()
        )
        attrs['calendar_obj'] = calendar_obj
        return attrs


class GetDateAppointmentSerializer(serializers.Serializer):
    date = serializers.DateField()
    end_date = serializers.DateField(allow_null=True, required=False, )


class MainDateTimeItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()


class MainDateTimeListSerializer(serializers.Serializer):
    date_list = serializers.ListSerializer(child=MainDateTimeItemSerializer())


class CalendarDateField(serializers.Field):
    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        return dateutil.parser.parse(data)


class SaveCalendarAppointmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    provider_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    start_date = CalendarDateField()
    start_time = serializers.TimeField(input_formats=["%I:%M %p"])
    end_time = serializers.TimeField(
        input_formats=["%I:%M %p"], required=False)
    end_date = CalendarDateField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    mobile = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    zip_code = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    email = serializers.EmailField(
        required=False, allow_null=True, allow_blank=True)
    note = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        id = attrs.get('id', None)
        provider_id = attrs.get('provider_id', None)
        service_id = attrs.get('service_id', None)
        email = attrs.get('email', None)
        start_date = attrs.get('start_date', None)
        start_time = attrs.get('start_time', None)
        end_time = attrs.get('end_time', None)
        end_date = attrs.get('end_date', None)
        first_name = attrs.get('first_name', None)
        last_name = attrs.get('last_name', None)
        address = attrs.get('address', None)
        city = attrs.get('city', None)
        phone = attrs.get('phone', None)
        phone = phone.encode('ascii', 'ignore') if phone else None
        mobile = attrs.get('mobile', None)
        zip_code = attrs.get('zip_code', None)
        note = attrs.get('note', None)
        users_provider_obj: Account = get_object_or_404(
            Account, id=provider_id)
        services_obj = Service.objects.filter(id=service_id).first()

        account_obj: Account = Account.get_customer(
            users_provider_obj.generalsettings_id, email=email, phone=phone)

        if account_obj:
            # update the customer data
            account_obj.username = email
            account_obj.name = first_name
            account_obj.last_name = last_name
            account_obj.phone = phone
            account_obj.mobile = mobile
            account_obj.address = address
            account_obj.city = city
            account_obj.zip_code = zip_code
            account_obj.note = note
            account_obj.save()
        else:

            # check that the mail ID is safe to be used for new user
            if email is not None and Account.registered_with_email_id(email_id=email,
                                                                      company_id=users_provider_obj.generalsettings_id):
                raise ValidationError(
                    {'email': "This E-Mail ID is already registered with us."})

            # create customer record for the provider
            account_obj = Account.objects.create(
                email=email,
                name=first_name,
                last_name=last_name,
                phone=phone,
                mobile=mobile,
                address=address,
                city=city,
                zip_code=zip_code,
                note=note,
                is_customers=True,
                generalsettings=users_provider_obj.generalsettings
            )

        start_time = datetime.combine(start_date, start_time)
        end_time = datetime.combine(
            end_date, end_time) if end_date and end_time else None

        attrs['account_obj'] = account_obj
        attrs['calendar_obj'] = CalendarDb.add_or_reschedule_appointment(
            provider=users_provider_obj,
            customer=attrs.get('account_obj'),
            service=services_obj,
            start_time=start_time,
            end_time=end_time,
            note=note,
            appointment_id=id,
        )
        return attrs
