"""to test the distribution after `zappa package`"""

from .local import *

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
