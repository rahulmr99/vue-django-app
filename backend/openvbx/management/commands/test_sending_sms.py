from django.core.management.base import BaseCommand
from openvbx.utils import send_sms


class Command(BaseCommand):
    help = "Trigger a twilio SMS"

    def add_arguments(self, parser):
        parser.add_argument('to', help='Target Number with country code. e.g. +91987654321')
        parser.add_argument('--text', help='SMS body', default='test messsage ...')

    def handle(self, *args, **options):
        send_sms(to=options['to'], body=options['text'])
