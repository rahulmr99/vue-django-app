from rest_framework import serializers

from . import models


class VoiceMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoiceMail
        fields = '__all__'


class VoiceMailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoiceMailConfig
        fields = [
            'id',
            'generalsettings',
            'greeting_message',
            'use_audio',
            'greeting_voice',
            'greeting_voice_filename',
        ]

    greeting_voice_filename = serializers.SerializerMethodField(required=False, allow_null=True, )

    def get_greeting_voice_filename(self, obj: models.VoiceMailConfig):
        return obj.greeting_voice.name if obj.greeting_voice else ''
