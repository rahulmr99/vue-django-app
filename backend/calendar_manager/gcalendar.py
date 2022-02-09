"""module to google calendar related work"""
import logging

import httplib2
import pytz
from datetime import timedelta
from django.utils import timezone
from googleapiclient import discovery
from oauth2client.client import OAuth2Credentials
from oauth2client.contrib.django_util.storage import DjangoORMStorage

from lexbot.handlers import utils
from authentication_user.models import GoogleCredentials
logger = logging.getLogger(__file__)


def build_event_obj(calendardb, tzname=False) -> dict:
    # appointment_time: timedelta = calendardb.start_datetime - timezone.now()

    # Each provider have different timezone so when adding booking date time to gcalndar
    # Make sure date time is converted to providers timezone
    
    if tzname:
        tzname = 'US/Eastern' if tzname == 'EST' else tzname
        tz_obj = pytz.timezone(tzname)
        start_datetime = calendardb.start_datetime.astimezone(tz_obj)
        end_datetime = calendardb.end_datetime.astimezone(tz_obj)
        
        start_time = start_datetime.isoformat()
        end_time = end_datetime.isoformat()
    else:
        start_time = calendardb.start_time_local.isoformat()
        end_time = calendardb.end_time_local.isoformat()

    logger.info('Done adding to google calendar {}'.format(start_time))
    
    return {
        'summary': f'{calendardb.users_customer.get_full_name()} : '
                   f'{calendardb.services.name if calendardb.services else ""}',
        # 'location': '800 Howard St., San Francisco, CA 94103',
        # 'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            #'dateTime': f'{calendardb.start_time_local.isoformat()}',
            'dateTime': f'{start_time}',
            'timeZone': f'{tzname}',
        },
        'end': {
            'dateTime': f'{end_time}',
            'timeZone': f'{tzname}',
        },
        'attendees': [
            # {'email': f'{calendardb.users_customer.email or ""}'},
        ],
        'reminders': {
            'useDefault': True,
            # 'overrides': [
            #     # {'method': 'email', 'minutes': int(calendardb.reminder_setting.send_time * 60)},
            #     # {'method': 'email', 'minutes': int((appointment_time.total_seconds() / 60) - 1)},
            #     # {'method': 'popup', 'minutes': 10},
            # ],
        },
    }


def build_http_service(calendardb):
    if not calendardb.users_provider_id:
        return
    provider = calendardb.users_provider
    storage = DjangoORMStorage(GoogleCredentials, 'id', provider, 'credential')
    credentials: OAuth2Credentials = storage.get()
    if not credentials or credentials.invalid:
        # todo: notify provider that the google events are not happening
        storage.delete()
        logging.error(f'Not able to create google calendar event. No credential available for the user {provider}')
        return

    if credentials and credentials.access_token_expired:
        # code to refresh token
        credentials.refresh(httplib2.Http())

    http = credentials.authorize(httplib2.Http())

    return discovery.build('calendar', 'v3', http=http, cache_discovery=False, )


def add_event(calendardb, reschedule: bool = False, tzname=False):
    """add/move calendar event in google calendar of the provider user"""

    event = build_event_obj(calendardb, tzname)
    service = build_http_service(calendardb)
    if not service:
        return
    calendar_args = dict(calendarId='primary', body=event, sendNotifications=True, )
    if reschedule and calendardb.google_calendar_event_id:
        eventRequest = service.events().update(**calendar_args, eventId=calendardb.google_calendar_event_id)
    else:
        eventRequest = service.events().insert(**calendar_args)
    event = eventRequest.execute()
    calendardb.google_calendar_event_link = event.get("htmlLink")
    calendardb.google_calendar_event_id = event.get("id")
    calendardb.save()
    logging.info(f'Google calendar Event created: {event.get("htmlLink")}')


def remove_event(calendardb):
    """remove google calendar event"""
    service = build_http_service(calendardb)
    if (not service) or (not calendardb.google_calendar_event_id):
        return
    calendar_args = dict(calendarId='primary', eventId=calendardb.google_calendar_event_id)
    service.events().delete(**calendar_args).execute()


if __name__ == '__main__':
    # quick test
    from calendar_manager.models import CalendarDb

    add_event(CalendarDb.objects.get(pk=91))
