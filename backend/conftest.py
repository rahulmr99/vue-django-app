"""pytest fixtures and helpers"""

import copy
import pytest

from model_mommy import mommy
from rest_framework.test import APIClient
from utils_plus.utils import reverse_url

from authentication_user.models import Account
from lexbot.tests.data import TEST_TWILIO_MSG_DATA

# import fixtures from other packages
pytest_plugins = ['lexbot.tests.fixtures', 'calendar_manager.tests.fixtures', 'openvbx.tests.fixtures']


@pytest.fixture
def account_factory(db):
    """creates new account"""

    def _create_account(**attrs) -> Account:
        if attrs.get('is_root_user'):
            attrs.update(dict(generalsettings_id=None))
            if 'email' not in attrs:
                attrs['email'] = 'root@mail.com'

        account: Account = mommy.make(Account, **attrs)
        password = attrs.get('password')
        if password:
            account.set_password(password)
            account.save()
            # set this attribute for later use in testing
            account.raw_password = password
        return account

    return _create_account


@pytest.fixture
def root_user(account_factory) -> Account:
    # return account_factory(is_root_user=True, password='pwd', timezone='EST')
    return account_factory(is_root_user=True, password='pwd')


@pytest.fixture
def twilio_post_data(db):
    """a copy of sample event data to test with handlers. This can be modified inside the test and wont affect others"""
    return copy.deepcopy(TEST_TWILIO_MSG_DATA)


@pytest.fixture
def phone_customer(account_factory, twilio_post_data, root_user):
    return account_factory(
        is_customers=True,
        phone=twilio_post_data['From'],
        generalsettings_id=root_user.generalsettings_id,
        email='customer@test.com',
    )


@pytest.fixture(name='apiclient')
def rest_api_client(root_user):
    """Django rest framework client logged in"""
    client = APIClient()
    resp = client.post(
        str(reverse_url('login_token')),
        dict(email=root_user.email, password=root_user.raw_password),
        format='json')
    if 'token' not in resp.data:
        pytest.fail(f"Failed to get API token. Response was {resp.data}")
    token = resp.data['token']
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    client.user = root_user
    yield client
