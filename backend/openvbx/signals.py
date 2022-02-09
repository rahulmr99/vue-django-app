from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import VoiceMail
from .utils import send_pusher_notification


@receiver(post_save, sender=VoiceMail)
def post_save_function(sender, instance, created, **kwargs):
    if created:
        send_pusher_notification(
            'bookedfusion', 'voicemail-created', {'generalsettings_id': instance.generalsettings_id}
        )
