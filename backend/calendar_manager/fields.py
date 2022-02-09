from django.utils import timezone
from rest_framework import serializers


class TzDateTimeField(serializers.DateTimeField):
    """when DRF return datetime , it sends as UTC. But we would want that in localtime"""

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super().to_representation(value)
