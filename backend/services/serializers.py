from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from authentication_user.models import Account
from services.models import Service, Category


class ServiceModelSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PublicServiceSerializer(serializers.Serializer):
    provider_id = serializers.IntegerField()

    def validate(self, attrs):
        provider_id = attrs.get('provider_id', None)
        attrs['provider_obj'] = get_object_or_404(Account, id=provider_id)
        return attrs
