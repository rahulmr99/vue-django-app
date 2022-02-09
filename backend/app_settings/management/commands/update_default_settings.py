from django.core.management.base import BaseCommand

from app_settings.abstracts import AbstractEmailModel
from app_settings.models import *
from authentication_user.models import Account
from services.models import Service


class Command(BaseCommand):
    help = "Update the mail templates in database"

    def handle(self, *args, **options):
        for gs in GeneralSettings.objects.all():
            gs.create_related_settings()
        for email_model in AbstractEmailModel.__subclasses__():
            for obj in email_model.objects.all():
                obj.set_defaults()
                obj.save()

        updated_recs = Account.objects.filter(is_active=False).update(is_active=None)
        if updated_recs:
            print('Update customer accounts: ', updated_recs)
        Account.objects.filter(email="root@gmail.com").update(is_superuser=True, is_staff=True)

        # update service models on existing objects
        for ac in Account.objects.filter().providers():
            Service.create_default_services(ac)
