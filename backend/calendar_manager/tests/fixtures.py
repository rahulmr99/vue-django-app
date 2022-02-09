"""pytest fixtures and helpers"""
import datetime
import pytest

MONDAY = 1
SUNDAY = 7


@pytest.fixture
def get_day_date():
    def _get_next_day(day_number: int, from_past=False, next=False) -> datetime.datetime:
        book_date = datetime.datetime.now()

        if next:
            book_date += datetime.timedelta(days=7)
        elif from_past:
            book_date -= datetime.timedelta(days=7)

        for i in range(8):
            if from_past:
                new_dt = book_date - datetime.timedelta(days=i)
            else:
                new_dt = book_date + datetime.timedelta(days=i)

            if new_dt.isoweekday() == day_number:
                return new_dt

    return _get_next_day


@pytest.fixture
def get_next_day_formatted(get_day_date):
    def _get_next_day_formatted(day_number: int) -> str:
        return get_day_date(day_number, next=True).strftime('%Y-%m-%d')

    return _get_next_day_formatted


@pytest.fixture
def next_sunday(get_next_day_formatted) -> str:
    """return datetime of next sunday"""
    return get_next_day_formatted(SUNDAY)


@pytest.fixture
def next_monday(get_next_day_formatted) -> str:
    """return datetime of next monday"""
    return get_next_day_formatted(MONDAY)


@pytest.fixture
def create_calendardb(root_user, phone_customer):
    def _create_calendardb(apt_date: datetime.date):
        from calendar_manager.models import CalendarDb

        day_number = apt_date.isoweekday()
        start_time = root_user.workingplan_set.get(day=day_number).start
        apt_time = datetime.datetime.combine(apt_date, start_time)
        service = root_user.services.first()

        apt = CalendarDb.add_or_reschedule_appointment(
            provider=root_user, customer=phone_customer, service=service, start_time=apt_time
        )
        return apt

    return _create_calendardb


@pytest.fixture
def next_monday_appointment(create_calendardb, get_day_date):
    apt_date = get_day_date(MONDAY, next=True).date()
    return create_calendardb(apt_date)


@pytest.fixture
def past_monday_appointment(create_calendardb, get_day_date):
    apt_date = get_day_date(MONDAY, from_past=True).date()
    return create_calendardb(apt_date)
