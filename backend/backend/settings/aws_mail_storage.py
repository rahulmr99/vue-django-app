from backend.config import CONFIG
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# -------- Aws --------
AWS_REGION = "us-east-2"
AWS_ACCESS_KEY_ID = CONFIG.APP_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = CONFIG.APP_AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = 'secure.bookedfusion.com'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

# -------django-s3-storage settings---------
AWS_S3_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
AWS_S3_KEY_PREFIX = "media"
AWS_S3_BUCKET_AUTH_STATIC = False
AWS_S3_BUCKET_NAME_STATIC = AWS_STORAGE_BUCKET_NAME
AWS_S3_MAX_AGE_SECONDS_CACHED_STATIC = 60 * 60 * 24 * 365  # 1 year.
AWS_S3_FILE_OVERWRITE_STATIC = True
AWS_S3_KEY_PREFIX_STATIC = AWS_LOCATION

# ------------- AWS SES Email --------
EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 465
# EMAIL_HOST_USER = 'AKIAIMQDOCRLECFNOO4A'
# EMAIL_HOST_PASSWORD = 'AiD7Fr3SJdczXklGm9ko3k8cpbAJqtxrvw3yEEhPYLPz'
ADMINS = [
    ('Noortheen', 'jnoortheen@gmail.com'),
    ('Michael', 'michaelsuccess35@gmail.com'),
    # ('Shahzad', 'shahzadfarukh100@gmail.com'),
]
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'michael@bookedfusion.com'
SERVER_EMAIL = 'michael@bookedfusion.com'
