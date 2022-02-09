from rest_framework.serializers import ModelSerializer

from .models import *


class CustomersModelSerializer(ModelSerializer):
    class Meta:
        model = Customers
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'city',
            'zip_code',
            'note'
        ]
