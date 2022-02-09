import boto3
import logging
import phonenumbers
import threading
from typing import Union

from backend.config import CONFIG
from lexbot.helpers.runtime_mappers import validate_session_attributes, LexRuntimeResponse
from services.models import Service

thread_locals = threading.local()


def parse_phone_number(number, region: str = None) -> (int, int):
    """
        parse phone number and return country code
    Args:
        number: actual number to validate may include '+' sign or in any standard format
        region: region code like US, IN

    Returns:
        tuple
    """
    num_args = [
        dict(number=number, region=region),
        dict(number=number),
    ]
    for kwargs in num_args:
        try:
            phonenumber = phonenumbers.parse(**kwargs)
            return phonenumber.national_number, phonenumber.country_code
        except Exception:
            pass
    raise Exception(f'Failed to parse phone number: {number}, region: {region}')


def get_or_create_customer_account(customer_account,
                                   phone_number: str,
                                   company_id: Union[str, int], first_name, last_name, **kwargs):
    from authentication_user.models import Account
    if customer_account is None:
        customer_account = Account(
            name=first_name,
            last_name=last_name,
            phone=phone_number,
            generalsettings_id=company_id,
            is_customers=True,
            **kwargs
        )
        customer_account.save()
    elif not customer_account.email and 'email' in kwargs:
        customer_account.email = kwargs['email']
        customer_account.save()

    return customer_account


def get_boto_client(service):
    return boto3.client(
        service,
        aws_access_key_id=CONFIG.APP_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=CONFIG.APP_AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
    )


def get_bot_response(user_id: str, input: str, session_store, req_attrs: dict = None, **kwargs) -> LexRuntimeResponse:
    """
        utility method to get response from lex bot and return response with object wrapper
    Args:
        user_id:
        input:
        req_attrs:
        **kwargs:
    """

    req_attrs = req_attrs or {}
    session_attrs = session_store.session_attrs

    # update the stored session attributes with user set one
    session_attrs.update(kwargs)

    logging.debug(f"Say: {input}")
    if not hasattr(thread_locals, 'client'):
        # by default boto3 clients are not thread safe. So create an instance per thread.
        thread_locals.client = get_boto_client('lex-runtime')

    client_kwargs = dict(
        botName='SMSBotRunTime',
        botAlias='$LATEST',
        userId=user_id,
        inputText=input,
    )

    if session_attrs:
        session_attrs['botType'] = 'SMS'
        client_kwargs['sessionAttributes'] = validate_session_attributes(session_attrs)
    if req_attrs:
        client_kwargs['requestAttributes'] = req_attrs

    resp = thread_locals.client.post_text(**client_kwargs)
    lex_resp = LexRuntimeResponse(resp)

    if lex_resp.is_fulfilled:
        session_store.delete()
    else:
        session_store.store(lex_resp.sessionAttributes)

    return lex_resp


def get_service(provider, returning_customer: str):
    returning_customer = int(returning_customer) if str(returning_customer).isdigit() else 0
    service_name = f"{'Returning' if returning_customer else 'New'} Patient"
    service = provider.services.filter(name=service_name).first()
    if not service:
        Service.create_default_services(provider)

    return service
