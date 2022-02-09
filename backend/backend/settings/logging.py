"""logging configs"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGGING_BASE_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'detail': {
            'format': '[%(levelname)s %(asctime)s] %(module)s %(process)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'detail'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'email-file': {
            'level': 'INFO',
            # 'class': 'logging.FileHandler',
            'class': 'logging.StreamHandler',
            # 'filename': os.path.join(LOGGING_BASE_DIR, 'email-details.log'),
            # 'encoding': 'utf8',
            'formatter': 'verbose',
        },
        'twillio-file': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            # 'class': 'logging.FileHandler',
            # 'filename': os.path.join(LOGGING_BASE_DIR, 'twillio.log'),
            # 'encoding': 'utf8',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', ],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console', ],
            'level': 'ERROR',
            'include_html': True,
            'propagate': True,
        },
        'email': {
            'handlers': ['email-file'],
            'level': 'INFO'
        },
        'sms': {
            'handlers': ['twillio-file'],
            'level': 'INFO'
        },
    }
}
