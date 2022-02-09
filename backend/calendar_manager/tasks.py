import logging

from zappa.async import task

logger = logging.getLogger(__file__)


@task

def add_to_google_calendar_task(calendar_pk, reschedule=False, remove=False, overide_delete=False, tzname=False):
    from .models import CalendarDb
    from . import gcalendar
    
    # trigger separate task to trigger google calendar save event
    try:
        calendardb = CalendarDb.objects.get(pk=calendar_pk)
    except CalendarDb.DoesNotExit:
        logger.error("Matching qurey doesn't exit")

    if remove and not overide_delete:
        logger.info(f'remove appointment from google calendar: {calendardb}, {calendar_pk}')
        gcalendar.remove_event(calendardb)
        logger.info('done removing appointment from google calendar')
    elif remove and overide_delete:
        logger.info(f'delete appointment from google calendar: {calendardb}, {calendar_pk}')
        try:
            gcalendar.remove_event(calendardb)
        except Exception as e:
            logger.error(e)
        logger.info('done deleting appointment from google calendar')
        calendardb.delete()
    else:
        logger.info('Adding to google calendar')
        gcalendar.add_event(calendardb, reschedule, tzname)
        logger.info('Done adding to google calendar')


@task
def async_run_calendar_func(calendar_pk, func_name: str):
    """call any of the mail functions of calendardb instance asynchronously"""
    from .models import CalendarDb
    logger.info(f'Run calendar method asynchronously: {func_name}')
    calendardb = CalendarDb.objects.get(pk=calendar_pk)
    getattr(calendardb, func_name)()
