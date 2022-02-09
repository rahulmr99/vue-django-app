"""pytest fixtures and helpers"""
import pytest


@pytest.fixture
def sms_outbox():
    from openvbx.utils import get_sms_outbox
    return get_sms_outbox()


@pytest.fixture
def faker():
    from faker import Faker
    return Faker()
