from django.core.management.base import BaseCommand

from authentication_user.models import Account
from services.models import Service


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        for account in Account.objects.filter(is_provider=True):
            Service.create_default_services(account)
        print('Added default services')
