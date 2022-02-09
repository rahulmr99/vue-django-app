import logging
from django.core.mail import EmailMultiAlternatives
from zappa.async import task

# from celery import shared_task
# from datetime import timedelta
from calendar_manager.tasks import async_run_calendar_func

_log_email = logging.getLogger('email')


@task
def send_html_mail(subject, html_content, to_emails, from_name=None, text_content=None, from_email='noreply@bookedfusion.com'):
    """a wrapper to send mails asynchronously using celery task"""

    if from_name:
        from_email = from_name + " " +'<noreply@bookedfusion.com>'
    else:
        from_email = 'noreply@bookedfusion.com'
    
    text_content = text_content or html_content
    to_emails = (to_emails if isinstance(to_emails, list) else [to_emails])
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to_emails)
    msg.attach_alternative(html_content, "text/html")
    _log_email.info(f'Send {subject} email to: {to_emails}')
    try:
        msg.send()
    except Exception as e:
        _log_email.error(str(e))


# @periodic_task(run_every=timedelta(minutes=5))
def send_reminder_emails():
    """ the scheduled task to send reminders to all appointments"""
    _log_email.info('Running scheduled task to send reminders')
    from calendar_manager.models import CalendarDb
    for calendardb in CalendarDb.objects.has_reminders().distinct():
        # call task asynchronously in their own lambda function to solve timeout problems
        _log_email.info(f'Running Async lambda task to send reminder for {calendardb}')
        async_run_calendar_func(calendardb.pk, 'send_reminders')


def send_feedback_emails():
    """zappa periodic task to send feedback emails for all appointments"""
    from calendar_manager.models import CalendarDb

    _log_email.info('Running scheduled task to send feedback emails')

    for calendardb in (
            CalendarDb.objects
                    .select_related('users_provider__generalsettings__feedbackconfig')
                    .waiting_for_feedback().distinct()
    ):
        fc = calendardb.feedback_setting
        # Send feedback email only if its enabled
        if fc.send:
            # send feedback mail after 4 hours from now
            calendardb.send_feedback_email()
            calendardb.sent_feedback_mail = True
            calendardb.save()
