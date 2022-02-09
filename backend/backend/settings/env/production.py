# noinspection PyUnresolvedReferences
from ..base import *
from ..aws_mail_storage import *
from backend.config import CONFIG

ALLOWED_HOSTS = ['.bookedfusion.com', '.execute-api.us-east-1.amazonaws.com', ]

# ---------static ----------
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'django_s3_storage.storage.ManifestStaticS3Storage'
STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'

# ------------ media files -----------
# AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
# PUBLIC_FILE_STORAGE = 'backend.storage_backends.PublicMediaStorage'
AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'

# import os

# if os.environ.get('SERVERTYPE') == 'AWS Lambda':
#     MIDDLEWARE.insert(0, 'aws_xray_sdk.ext.django.middleware.XRayMiddleware')


# backup settings
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': CONFIG.APP_AWS_ACCESS_KEY_ID,
    'secret_key': CONFIG.APP_AWS_SECRET_ACCESS_KEY,
    'bucket_name': 'secure.bookedfusion.com'
}
DBBACKUP_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
