from rest_framework import serializers
from authentication_user.models import Account


class RegisterUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()
    country_code = serializers.IntegerField()
    phone = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email', None)
        account_obj = Account.objects.filter(email=email).first()
        if account_obj is not None:
            # if account_obj.is_active or account_obj.is_root_user or account_obj.is_provider or account_obj.is_secretarie:
            raise serializers.ValidationError('Account already exists.')

        attrs['account_obj'] = account_obj
        return attrs


class SubscriptionSerializer(RegisterUserSerializer):
    stripe_token = serializers.CharField()
    plan_id = serializers.CharField()


class AccountSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
