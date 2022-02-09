from django.dispatch import receiver
from django_ses.signals import bounce_received, complaint_received

from authentication_user.choices import MAIL_STATUS
from authentication_user.models import Account
import logging

_log_email = logging.getLogger('email')


@receiver(bounce_received)
def bounce_handler(sender, *args, **kwargs):
    try:
        account = Account.objects.get(email=kwargs.get('mail_obj'))
        account.email_subscription_status = MAIL_STATUS.bounced.name
        account.save()
        _log_email.info(f'Received Email Bounce Notification for {account}')
    except Exception as ex:
        _log_email.error(f"Failed to handle email bounce signal {ex}")


@receiver(complaint_received)
def complaint_handler(sender, *args, **kwargs):
    try:
        account = Account.objects.get(email=kwargs.get('mail_obj'))
        account.email_subscription_status = MAIL_STATUS.complained.name
        account.save()
        _log_email.info(f'Received Email complaint for {account}')
    except Exception as ex:
        _log_email.error(f"Failed to handle email bounce signal {ex}")

# @receiver(complaint_received)
# def delivery_handler(sender, *args, **kwargs):
#     try:
#         account = Account.objects.get(email=kwargs.get('mail_obj'))
#         account.email_subscription_status = MAIL_STATUS..name
#         account.save()
#     except Exception as ex:
#         logging.error(f"Failed to handle email bounce signal {ex}")
