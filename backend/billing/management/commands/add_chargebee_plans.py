from django.core.management.base import BaseCommand

from billing.utils import create_plan


class Command(BaseCommand):
    help = "create payment plans"

    def handle(self, *args, **options):
        create_plan(name='Starter', amount=97)
        create_plan(name='Silver', amount=147)
        create_plan(name='Gold', amount=197)
