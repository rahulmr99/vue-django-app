from ..base import *

INSTALLED_APPS.append('django_smoke_tests')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
TEMPLATE_DEBUG = False
TESTS_IN_PROGRESS = True

# mock cache
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'default'
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.JustInTime'
DJANGO_TWILIO_FORGERY_PROTECTION = False

# mock sending sms. See `openvbx.utls.send_sms`
MOCK_SMS = True
