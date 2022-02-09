from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from app_settings.models import FeedbackConfig
from ratings_manager.models import Feedback


def trigger_validator(value):
    if len(value) > 200:
        raise serializers.ValidationError("Only 200 characters are allowed. Use https://tiny.cc/ to shorten url and then paste the link in here.")


class FeedbackConfigModelSerializer(ModelSerializer):
    google_rateus_link = serializers.URLField(validators=[trigger_validator])

    class Meta:
        model = FeedbackConfig
        fields = [
            'id',
            'generalsettings',
            'send',
            'send_time',
            'google_rateus_link',
            'yelp_rateus_link',
            'email_subject',
            'email_body',
        ]


class FeedbackModelSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
