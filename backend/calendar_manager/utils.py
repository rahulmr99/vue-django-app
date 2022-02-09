import pytz
import uuid
import datetime
from datetime import timedelta
from typing import List, Generator

from django.db.models import QuerySet
from django.utils import timezone


from app_settings.models import WorkingPlan


def get_day_list(page: int, user=None) -> List[datetime.datetime]:
    """

    Args:
        page:

    Returns:
    """
    start = page * 5
    tzname = user.timezone if user else 'EST'
    tzname = pytz.timezone(tzname)

    return [timezone.now().replace(tzinfo=None).astimezone(tzname) + datetime.timedelta(days=x) for x in range(start, start + 5)]


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
        aaa = end - current
        if aaa < delta:
            break


def check_list(slot_to_check: datetime.datetime, active_appointments, provider_timezone=None, converted_tz=False) -> bool:
    return active_appointments.is_overlapping(slot_to_check, tzname=provider_timezone, converted_tz=converted_tz)


def check_breaks(slot_time: datetime.datetime, breaks: QuerySet) -> bool:
    """

    Args:
        slot_time:
        breaks:

    Returns:
        bool: return true if any of the swarm has slot time included
    """
    return breaks.filter(start__lte=slot_time.time(), end__gt=slot_time.time(), day=slot_time.isoweekday()).exists()


def caption_maker(date):
    time_now = timezone.localtime(timezone.now())
    if date.date() == time_now.date():
        return 'Today'
    elif date.date() == (time_now + datetime.timedelta(days=1)).date():
        return 'Tomorrow'
    elif date.weekday() == 6:
        week_count = round((date - time_now).days / 6)
        if week_count == 0:
            return 'Next week'
        else:
            return 'in {} week'.format(week_count)
    else:
        return ''


def filter_a_days_slots(
        day: datetime.datetime,
        providers_working_plan: WorkingPlan,
        interval: datetime.timedelta,
        providers_calendar_tasks,
        providers_breaks,
        user=None
) -> Generator[datetime.datetime, None, None]:
    providers_calendar_tasks = providers_calendar_tasks.filter(
        start_datetime__contains=day.date()
    ).active_appointments()

    tzname = user.timezone if user else 'US/Eastern'
    tzname = 'US/Eastern' if tzname == "EST" else tzname

    tz_obj = pytz.timezone(tzname)
    timezone.activate(tz_obj)

    day = day.astimezone(tz_obj)
    for time_slot in datetime_range(
            day.replace(
                hour=providers_working_plan.start.hour,
                minute=providers_working_plan.start.minute,
                second=0,
                microsecond=0),
            day.replace(
                hour=providers_working_plan.end.hour,
                minute=providers_working_plan.end.minute,
                second=0,
                microsecond=0
            ),
            interval,
    ):
        if (
                time_slot >= timezone.now()  # do not show past time
                # do not show already booked slots
                and not check_list(time_slot, providers_calendar_tasks, provider_timezone=tz_obj, converted_tz=True)
                # do not include break hours
                and not check_breaks(time_slot, providers_breaks)
        ):
            yield time_slot


def get_filtered_time_slots(day: datetime.datetime, working_plans, interval: datetime.timedelta,
                            calendar_tasks: QuerySet, breaks,  user=None) -> list:
    new = []
    for timeslot in filter_a_days_slots(day, working_plans, interval, calendar_tasks, breaks, user=user):

        new.append({
            'time': timeslot,
            'date': timeslot,
            'choice': False,
            'block': False,
            'cancel': False,
            'datetime': timeslot,
            'key': timeslot.strftime('%s')
        })
    return new


def convert_dt_to_provider_timezone(calendar_obj, end_date=False):
    """
    Convert UTC date time back to the providers timezone
    """
    tzname = 'US/Eastern' if calendar_obj.users_provider.timezone and calendar_obj.users_provider.timezone == 'EST' else calendar_obj.users_provider.timezone
    tz_obj = pytz.timezone(tzname)

    if end_date:
        appt_date = calendar_obj.end_datetime.astimezone(tz_obj)
    else:
        appt_date = calendar_obj.start_datetime.astimezone(tz_obj)

    return appt_date
