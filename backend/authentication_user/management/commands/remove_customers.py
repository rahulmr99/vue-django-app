from django.core.management.base import BaseCommand

from authentication_user.models import Account
from services.models import Service


class Command(BaseCommand):
    help = "Remove customers management command."

    def handle(self, *args, **options):
        Account.objects.filter(is_customers=True).all().delete()
