from django.db import models
from django_extensions.db.models import TimeStampedModel

from app_settings.models import GeneralSettings


class VoiceMail(TimeStampedModel):
    generalsettings = models.ForeignKey(GeneralSettings, on_delete=models.CASCADE, )
    callsid = models.CharField(max_length=40, unique=True, db_index=True, )
    recordingsid = models.CharField(max_length=40, blank=True, null=True, )
    transcriptionsid = models.CharField(max_length=40, blank=True, null=True, )

    from_caller_id = models.CharField(max_length=20, null=True, blank=True)
    '''caller phone number'''
    to_caller_id = models.CharField(max_length=20, null=True, blank=True)
    '''receiver phone number'''

    recording_url = models.URLField(null=True, blank=True, )
    '''twilio url where the recorded message is saved'''
    recorded_file = models.FileField(null=True, blank=True, upload_to='voicemails/%Y/%m/%d/')
    '''django media file'''

    duration = models.DurationField(null=True, blank=True)
    transcription_text = models.TextField(default='Voice is being transcribed...')


class VoiceMailConfig(models.Model):
    class Meta:
        ordering = ['-id', ]

    generalsettings = models.OneToOneField(GeneralSettings, on_delete=models.CASCADE, )
    greeting_message = models.CharField(max_length=200, default='Hello. Please leave a message after the beep.')
    use_audio = models.BooleanField(default=False, )
    greeting_voice = models.FileField(null=True, blank=True, )

    def __str__(self):
        return f"Voice Config of: {self.generalsettings}"
