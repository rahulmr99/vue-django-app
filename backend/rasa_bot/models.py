import datetime
import json
import logging
import pytz
from django.conf import settings
from django.db import models
from django_mysql.models import JSONField
from django_extensions.db.models import TimeStampedModel


class RasaBotUserSession(TimeStampedModel):
    """Keep rasa bot user session"""

    # User id - Phone number
    user_id = models.CharField(
        max_length=200, db_index=True, unique=True, primary_key=True)

    message_id = models.CharField(max_length=200)
    from_no = models.CharField(max_length=100, null=True, blank=True)
    to_no = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    
    EXPIRE_TIME_SECS = 10 * 60
    '''users session attributes will expire if there is no activity in last 10 mins.'''