from datetime import datetime, timedelta
from model_mommy import mommy
from rest_framework.test import APIClient
from utils_plus.utils import reverse_url

from authentication_user.models import Account
from calendar_manager.models import CalendarDb
from services.models import Service


# def test_create_calendar(db, root_user: Account, mailoutbox, phone_customer):
#     service: Service = root_user.services.first()
#     time = datetime.now()
#     calendardb = CalendarDb.add_or_reschedule_appointment(
#         provider=root_user, customer=phone_customer, service=service, start_time=time
#     )

#     # time = time + timedelta(hours=1)
#     assert (calendardb.end_datetime - calendardb.start_datetime).seconds == timedelta(minutes=service.duration).seconds
#     assert CalendarDb.objects.count() == 1
#     assert calendardb.start_time_local.hour == time.hour
#     assert calendardb.start_time_local.minute == time.minute
#     assert len(mailoutbox) == 2
#     assert calendardb.get_email_context()['oldtime'] == ''


# def test_reschedule_calendar(phone_customer, root_user: Account, mailoutbox):
#     service: Service = root_user.services.first()
#     time = datetime.now()

#     kwargs = dict(provider=root_user, customer=phone_customer, service=service, start_time=time)
#     calendardb = CalendarDb.add_or_reschedule_appointment(**kwargs)
#     assert CalendarDb.objects.count() == 1

#     # start rescheduling existing appointment
#     resch_time = time + timedelta(days=2)
#     kwargs['start_time'] = resch_time
#     calendardb = CalendarDb.add_or_reschedule_appointment(**kwargs, appointment_id=calendardb.pk)

#     # resch_time = resch_time + timedelta(hours=1)
#     assert CalendarDb.objects.count() == 1
#     assert calendardb.start_time_local.hour == resch_time.hour
#     assert calendardb.start_time_local.minute == resch_time.minute
#     assert len(mailoutbox) == 4
#     assert calendardb.get_email_context()['oldtime']


# def assert_appointments_count(apiclient, start_date, end_date, assert_count: int):
#     """helper function"""
#     resp: dict = apiclient.post(
#         reverse_url('api_v1:calendardb-get-main-calendar-from-date'),
#         dict(date=str(start_date.date()), end_date=str(end_date.date())), format='json'
#     ).data
#     assert CalendarDb.objects.count() == assert_count
#     assert len(resp) == assert_count


# def test_get_main_calendar_from_date(db, apiclient: APIClient, get_next_day_formatted, mailoutbox):
    # today = datetime.today()
    # end_date = today + timedelta(days=30)
    # provider: Account = apiclient.user
    # service = mommy.make(Service, duration=20)

    # # check there is no appointment for the provider
    # assert_appointments_count(apiclient, today, end_date, assert_count=0)

    # # create appointments
    # print(apiclient.post(
    #     reverse_url('api_v1:calendardb-save-calendar-appointment'),
    #     dict(
    #         provider_id=provider.id, service_id=service.id,
    #         start_date=get_next_day_formatted(1),  # Monday
    #         start_time="10:00 AM",
    #         first_name='First', last_name='Last',
    #         phone='123567890', email='customer@mail.com',
    #     )
    # ).data)

    # # check there is one appointment
    # assert_appointments_count(apiclient, today, end_date, assert_count=1)

    # print(apiclient.post(
    #     reverse_url('api_v1:calendardb-save-calendar-appointment'),
    #     dict(
    #         provider_id=provider.id, service_id=service.id,
    #         start_date=get_next_day_formatted(2),
    #         start_time='10:00 AM',
    #         first_name='First', last_name='Last',
    #         phone='123567890', email='customer@mail.com',
    #     )
    # ).data)

    # # check there is TWO appointment for the provider
    # assert_appointments_count(apiclient, today, end_date, assert_count=2)

    # assert len(mailoutbox) == 4
