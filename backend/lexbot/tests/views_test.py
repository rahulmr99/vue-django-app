from django.test import RequestFactory
from unittest.mock import MagicMock
from utils_plus.utils import reverse_url

from calendar_manager.models import CalendarDb
from lexbot import views
from lexbot.helpers.runtime_mappers import LexRuntimeResponse
from lexbot.tests.data import LEX_RESP


def get_sms_bot_url(company_id):
    return str(reverse_url('bot:sms_bot_view', company_id))


def test_sms_bot_view(db, rf: RequestFactory, root_user, next_monday_appointment, twilio_post_data):
    assert CalendarDb.objects.count() == 1
    request = rf.post(get_sms_bot_url(root_user.generalsettings_id), twilio_post_data)

    # patch the bot call
    views.get_bot_response = MagicMock()
    views.get_bot_response.return_value = LexRuntimeResponse(LEX_RESP)

    resp = views.sms_bot_view(request, root_user.generalsettings_id)

    assert LEX_RESP['message'][20:] in str(resp.content)


def test_sms_bot_getting_email_id(db, rf: RequestFactory, root_user, twilio_post_data, faker):
    twilio_post_data['Body'] = f"email id is {faker.email()}"
    request = rf.post(get_sms_bot_url(root_user.generalsettings_id), twilio_post_data)

    resp = views.sms_bot_view(request, root_user.generalsettings_id)

    assert "we'll see you soon" in resp.content.decode()


def test_voice_bot_view(db, root_user, rf: RequestFactory, twilio_post_data):
    request = rf.post(get_sms_bot_url(root_user.generalsettings_id), twilio_post_data)

    # call view
    resp = views.voice_bot_view(request, root_user.generalsettings_id)
    assert 'Welcome' in str(resp.content)
    assert 'Press 1 to book' in str(resp.content)


def test_get_voice_bot_user_choice_book(db, root_user, rf: RequestFactory, twilio_post_data):
    twilio_post_data['Digits'] = '1'
    request = rf.post(str(reverse_url('bot:get_voice_bot_user_choice', root_user.generalsettings_id)), twilio_post_data)

    # call view
    resp = views.get_voice_bot_user_choice(request, root_user.generalsettings_id)
    assert str(views.AWS_CONNECT_BOOK_NUMBER) in str(resp.content)


def test_gather_user_phone_number(db, root_user, rf: RequestFactory, twilio_post_data):
    data = twilio_post_data
    data['Digits'] = twilio_post_data['From'][1:]
    request = rf.post(reverse_url('bot:gather_user_phone_number', root_user.generalsettings_id), data)

    # call view
    resp = views.gather_user_phone_number(request, root_user.generalsettings_id)
    assert str(reverse_url('bot:retry_gathering_user_phone_number', root_user.generalsettings_id)) in str(resp.content)


def test_retry_gathering_user_phone_number(db, root_user, rf: RequestFactory, twilio_post_data):
    data = twilio_post_data
    data['Digits'] = twilio_post_data['From'][1:]
    request = rf.post(reverse_url('bot:retry_gathering_user_phone_number', root_user.generalsettings_id), data)

    # call view
    resp = views.retry_gathering_user_phone_number(request, root_user.generalsettings_id)
    assert "https://s3.amazonaws.com/bookedfusion.com/checks+phone+number+audios/3rd+response+if+" in resp.content.decode()
