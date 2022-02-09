"""pytest fixtures and helpers"""

import copy
import pytest

from lexbot.tests.data import AWS_CONTACTFLOW_EVENT
from lexbot.tests.data import LEX_EVENT
from lexbot.tests.helpers import LexBotMock


@pytest.fixture
def lex_event_data(twilio_post_data, root_user):
    """a copy of sample event data to test with handlers"""
    data = copy.deepcopy(LEX_EVENT)
    data['sessionAttributes'] = dict(
        callerPhoneNumber=twilio_post_data['From'],
        providerPhoneNumber=twilio_post_data['To'],
        company_id=str(root_user.generalsettings_id),
    )
    return data


@pytest.fixture
def aws_connect_flow_data():
    """a copy of sample event data to test with handlers"""

    def _aws_conntect_data(func_name: str):
        data = copy.deepcopy(AWS_CONTACTFLOW_EVENT)
        data['Details']['Parameters']['InvokeFunction'] = func_name
        return data

    return _aws_conntect_data


@pytest.fixture
def lexbot_book(lex_event_data) -> LexBotMock:
    """a copy of sample event data to test with handlers"""
    from lexbot.handlers.sms import schedule

    mock = LexBotMock(data=lex_event_data, handler=schedule.handler)
    return mock


@pytest.fixture
def lexbot_cancel(lex_event_data) -> LexBotMock:
    """a copy of sample event data to test with handlers"""
    from lexbot.handlers.sms import cancel

    mock = LexBotMock(data=lex_event_data, handler=cancel.handler)
    return mock


@pytest.fixture
def callerinfo_creator(root_user, twilio_post_data, rf, ):
    """function based fixture to create callerinfo with given attributes"""
    from lexbot import views, models
    from lexbot.tests.views_test import get_sms_bot_url

    def _create_callerinfo(digit: str):
        # call view to create a callerinfoqueue record
        twilio_post_data['Digits'] = digit
        request = rf.post(get_sms_bot_url(root_user.generalsettings_id), twilio_post_data)
        views.get_voice_bot_user_choice(request, root_user.generalsettings_id)
        return models.CallerInfoQueue.get_caller_info(twilio_post_data['From'], delete=False)

    return _create_callerinfo


@pytest.fixture(autouse=True)
def dynamodb():
    """create test tables and destroy them at the end of the test"""
    yield
    from pynamodb.models import Model
    for Table in Model.__subclasses__():
        if Table.Meta.table_name.startswith("test-"):
            for rec in Table.scan():
                rec.delete()
