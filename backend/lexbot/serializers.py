from rest_framework import serializers

from . import models


class VoiceBotConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoiceBotConfig
        fields = [
            'id',
            'generalsettings',
            'greeting_message',
            'use_audio',
            'greeting_voice',
            'greeting_voice_filename',
            'redirect_to_browser',
            'redirect_telephone_number',
        ]

    greeting_voice_filename = serializers.SerializerMethodField(required=False, allow_null=True, )

    def get_greeting_voice_filename(self, obj: models.VoiceBotConfig):
        return obj.greeting_voice.name if obj.greeting_voice else ''
