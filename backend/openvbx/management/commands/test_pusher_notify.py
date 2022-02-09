import datetime
from django.core.management.base import BaseCommand
from openvbx.utils import send_pusher_notification


class Command(BaseCommand):
    help = "Trigger a pusher notification"

    def handle(self, *args, **options):
        send_pusher_notification("Test", "Test", {"test": str(datetime.datetime.now())})
