import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update the mail templates in database"

    def handle(self, *args, **options):
        for func in [self.print_config, self.test_twilio_endpoint, self.ssl_health]:
            try:
                print('Run: ', func)
                func()
            except Exception as ex:
                print(ex)

    def print_config(self):
        from backend.config import CONFIG
        print("Config:")
        for attr in CONFIG.__dict__:
            if not attr.startswith('__'):
                print('\t', attr, ':', getattr(CONFIG, attr))
        print("Env: ")
        for attr in os.environ:
            print('\t', attr, ':', os.environ[attr])

    def test_twilio_endpoint(self):
        import requests
        from django.conf import settings
        request = requests.get(
            f'https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json',
            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN))
        print(request.json())

    def ssl_health(self):
        import requests
        print(requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])
