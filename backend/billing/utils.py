import json

import chargebee
from django.conf import settings

from authentication_user.models import Account
from .models import Subscription


def auth_chargebee():
    chargebee.configure(settings.CHARGEBEE_API_KEY, settings.CHARGEBEE_WEBSITE)


def create_plan(name, amount):
    """
    :param name: Name of plan
    :param amount: amount of plan (in USD)
    :return: void
    """
    auth_chargebee()
    try:
        chargebee.Plan.create({
            "id": "{}".format(name.lower()),
            "name": "{}".format(name.capitalize()),
            "invoice_name": "{} membership".format(name.capitalize()),
            "price": amount * 100,
            "period": 1,
            "period_unit": "month",
            "trial_period_unit": "day",
            "trial_period": 14,
            "currency_code": "USD"
        })
    except Exception as e:
        print(e)
        raise ChargebeeError('Error while creating plan', exact=e)


def rollback_customer(user_account):
    # get updated account
    user_account = Account.objects.get(id=user_account.id)
    chargebee_cus_id = user_account.chargebee_customer_id
    if chargebee_cus_id:
        auth_chargebee()
        try:
            chargebee.Customer.delete(chargebee_cus_id)
        except Exception as e:
            print(e)
    user_account.delete()


def create_subscription(user_account, plan_id, stripe_token):
    try:
        _ = Subscription.objects.get(account=user_account)
        raise ChargebeeError('Error while creating subscription', exact='Subscription already exists')
    except Subscription.DoesNotExist:
        pass

    auth_chargebee()

    try:
        result = chargebee.Subscription.create({
            'plan_id': plan_id,
            'customer': {
                "email": user_account.email,
                "first_name": user_account.name,
                "last_name": user_account.last_name,
            },
            "billing_address": {
                "first_name": user_account.name,
                "last_name": user_account.last_name,
                "city": user_account.city,
                "state": user_account.state,
                "zip": user_account.zip_code,
                "country": user_account.region_code,
                "phone": user_account.phone,
                "line1": user_account.address
            },
            'payment_method': {
                'type': 'card',
                'gateway': 'stripe',
                'tmp_token': stripe_token
            }
        })
    except Exception as e:
        print(e)
        raise ChargebeeError('Error while creating subscription', exact=e)
    Subscription.objects.create(account=user_account, chargebee_subscription_id=result.subscription.id)
    user_account.chargebee_customer_id = result.customer.id
    user_account.save()


def cancel_subscription(user_account_id):
    auth_chargebee()
    try:
        subscription = Subscription.objects.get(account_id=user_account_id)
    except Subscription.DoesNotExist:
        raise ChargebeeError('Error while cancelling subscription', exact='Subscription does not exist')

    try:
        result = chargebee.Subscription.cancel(subscription.chargebee_subscription_id, {
            'end_of_term': True
        })
    except Exception as e:
        raise ChargebeeError('Error while cancelling subscription', exact=e)

    return result.subscription.cancelled_at


def get_subscription(user_account_id):
    auth_chargebee()
    try:
        subscription = Subscription.objects.get(account_id=user_account_id)
    except Subscription.DoesNotExist:
        raise ChargebeeError('Error while retrieving subscription user', exact='Subscription does not exist')

    try:
        result = chargebee.Subscription.retrieve(subscription.chargebee_subscription_id)
    except Exception as e:
        raise ChargebeeError('Error while retrieving subscription detail', exact=e)

    return load_result(result)['subscription']


def reactivate_subscription(user_account_id):
    auth_chargebee()
    try:
        subscription = Subscription.objects.get(account_id=user_account_id)
    except Subscription.DoesNotExist:
        raise ChargebeeError('Error while reactivating subscription', exact='Subscription does not exist')

    try:
        result = chargebee.Subscription.reactivate(subscription.chargebee_subscription_id, {
            'end_of_term': True
        })
    except Exception as e:
        raise ChargebeeError('Error while reactivating subscription', exact=e)

    return result.subscription.activated_at


def check_status(status_):
    status_dict = {
        'active': status_ == 'active',
        'in_future': status_ == 'future',
        "cancelled": status_ == 'cancelled',
        'non_renewing': status_ == 'non_renewing',
        'trial': status_ == 'in_trial',
        'paused': status_ == 'paused',
    }
    return status_dict


def load_result(result):
    return json.loads(str(result))


class ChargebeeError(Exception):
    def __init__(self, *args, **kwargs):
        self.exact = kwargs.pop('exact')
        super(ChargebeeError, self).__init__(*args, **kwargs)
