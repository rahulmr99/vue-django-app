import os
from django.conf import settings
import logging

settings.INSTALLED_APPS.append('qinspect')
settings.MIDDLEWARE.insert(0, 'qinspect.middleware.QueryInspectMiddleware')

NPLUSONE_LOGGER = logging.getLogger('nplusone')  # set the same for handler in logging settings
NPLUSONE_LOG_LEVEL = logging.WARN
_LOG_FILE_SIZE = 1024 * 1000


# there should be logger handler defined with the name console_debug
# def skip_0sql_requests(record: logging.LogRecord):
#     """do not log when the request is not interacting with database"""
#     skip_ptrn = '[SQL] 0 queries'
#     return not record.msg.startswith(skip_ptrn)


# settings.LOGGING['filters']['qinspect_filter_0_queries'] = {
#     # use Django's built in CallbackFilter to point to your filter
#     '()': 'django.utils.log.CallbackFilter',
#     # 'callback': skip_0sql_requests
# }
# settings.LOGGING['filters']['qinspect_req_debug_true'] = {
#     '()': 'django.utils.log.RequireDebugTrue',
# }
settings.LOGGING['handlers']['qinspect'] = {
    'level': 'DEBUG',
    # 'filters': ['qinspect_filter_0_queries', 'qinspect_req_debug_true', ],
    'class': 'logging.StreamHandler',
    'formatter': 'detail'
}
# settings.LOGGING['handlers']['qinspect_file'] = {
#     'level': 'DEBUG',
#     'class': 'logging.handlers.RotatingFileHandler',
#     'filename': os.path.join(os.path.dirname(os.path.abspath(__name__)), "logs", "qinspect.log"),
#     'maxBytes': _LOG_FILE_SIZE,
#     'backupCount': 10,
#     'formatter': 'detail',
#     'filters': ['qinspect_filter_0_queries', 'qinspect_req_debug_true', ],
# }
settings.LOGGING['loggers']['qinspect'] = {
    'handlers': ['qinspect',
                 # 'qinspect_file',
                 ],
    'level': 'DEBUG',
    'propagate': True,
}

# Whether the Query Inspector should do anything (default: False)
QUERY_INSPECT_ENABLED = True
# Whether to log the stats via Django logging (default: True)
QUERY_INSPECT_LOG_STATS = True
# Whether to add stats headers (default: True)
QUERY_INSPECT_HEADER_STATS = True
# Whether to log duplicate queries (default: False)
QUERY_INSPECT_LOG_QUERIES = True
# Whether to log queries that are above an absolute limit (default: None - disabled)
# QUERY_INSPECT_ABSOLUTE_LIMIT = 100  # in milliseconds
# Whether to log queries that are more than X standard deviations above the mean query time (default: None - disabled)
QUERY_INSPECT_STANDARD_DEVIATION_LIMIT = 2
# Whether to include tracebacks in the logs (default: False)
QUERY_INSPECT_LOG_TRACEBACKS = True
# Project root (a list of directories, see below - default empty)
QUERY_INSPECT_TRACEBACK_ROOTS = [os.path.abspath(os.path.dirname(__name__)), ]
