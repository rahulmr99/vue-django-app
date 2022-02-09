from ..base import *  # noqa
# noinspection PyUnresolvedReferences
from ..aws_mail_storage import *  # noqa

DEBUG = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
ALLOWED_HOSTS = ['.ngrok.io', 'localhost', '127.0.0.1', '.serveo.net', ]

# print emails to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# reloads any changes in static files
INSTALLED_APPS.insert(3, 'whitenoise.runserver_nostatic', )
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware', )

# do not send actual sms
MOCK_SMS = True
