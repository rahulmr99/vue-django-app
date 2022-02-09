import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from . import models
from calendar_manager.models import CalendarDb


class AccountModelSerializer(ModelSerializer):
    generalsettings = serializers.PrimaryKeyRelatedField(
        queryset=models.GeneralSettings.objects.all(),
        required=False
    )
    next_appoinment = serializers.SerializerMethodField()
    class Meta:
        model = models.Account
        exclude = ['token', 'restore', ]
        extra_kwargs = {'generalsettings': {'read_only': False}}

    def get_next_appoinment(self, obj):
        try:
            date = CalendarDb.objects.filter(users_customer=obj).latest('start_datetime').start_datetime
            if date.date() >= datetime.datetime.now().date():
                return date.date()
        except CalendarDb.DoesNotExist:
            pass
        return None


class CustomerModelWithoutUniqueValidatorSerializer(ModelSerializer):
    """
    Creating appointment from booking button getting unique together validation error.
    Already validating email and phone number in the viewset so safely disabling the unique validator
    Then only we can access the already existing unique together values from serilizer validated data
    https://stackoverflow.com/questions/45999131/django-rest-framework-model-serializer-with-out-unique-together-validation
    """
    class Meta():
        model = models.CustomerAccount
        fields = ('name', 'last_name', 'email', 'phone', 'note', 'id', 'generalsettings')

    def get_unique_together_validators(self):
        """
        Overriding method to disable unique together checks
        """
        return []

class CustomerModelSerializer(ModelSerializer):
    class Meta():
        model = models.CustomerAccount
        fields = ('name', 'last_name', 'email', 'phone', 'note', 'id')


class PublicProvidersModelSerializer(ModelSerializer):
    enabled_google_api = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Account
        fields = [
            'id',
            'username',
            'generalsettings_id',
            'name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'address',
            'state',
            'city',
            'zip_code',
            'note',
            'timezone',
            'providers',
            'services',
            'receive_notification',
            'is_admin',
            'is_provider',
            'is_secretarie',
            'appointment_interval',
            'enabled_google_api'
        ]


class CreateCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False)
    zip_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    datetime = serializers.DateTimeField()
    provider = serializers.IntegerField()
    service = serializers.IntegerField()
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class UpdateCalendarSerializer(serializers.Serializer):
    calendar_id = serializers.IntegerField()
    datetime = serializers.DateTimeField()
    service = serializers.IntegerField()


class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    # username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email', None)
        # username = attrs.get('username', None)
        password1 = attrs.get('password1', None)
        password2 = attrs.get('password2', None)
        account_obj = models.Account.objects.filter(email=email)
        if account_obj.exists():
            attrs['account_obj'] = account_obj.first()
        else:
            raise serializers.ValidationError('User error.')
        if password1 != password2:
            raise serializers.ValidationError('Invalid password.')
        return attrs


class CheckEmailExistsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        if not models.Account.objects.filter(email=email).exists():
            raise serializers.ValidationError("Please check you Email ID.")
        return attrs


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email', None)
        password1 = attrs.get('password1', None)
        password2 = attrs.get('password2', None)
        account_obj = models.Account.objects.filter(email=email)
        if account_obj.exists():
            attrs['account_obj'] = account_obj.first()
        else:
            attrs['account_obj'] = None
        if password1 != password2:
            raise serializers.ValidationError('Invalid password.')
        return attrs


class ConfirmPasswordReset(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        from rest_framework.generics import get_object_or_404

        email = attrs['email']

        # check account exists
        attrs['account'] = get_object_or_404(models.Account.objects.filter().authorizables(), email=email)

        # check confirmation code
        if not models.ConfirmationCode.validate_confirmation_code(attrs['code'], email):
            raise serializers.ValidationError('Confirmation code is not valid')
        return attrs
