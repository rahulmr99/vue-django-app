from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import Account


def decode_user(uidb64, token):
    """
        from the token and id returns the user object if they are valid
    Args:
        uidb64:
        token:

    Returns:
        Union[CalendarDb, None]:
    """

    if uidb64 is not None and token is not None:
        uid = urlsafe_base64_decode(uidb64)
        try:
            user = Account.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                return user
        except:
            pass


def encode_user(account):
    """
        return user_id and a token to be used in email links
    Args:
        account (Account):

    Returns:
        uidb64, token:
    """
    return urlsafe_base64_encode(force_bytes(account.pk)), default_token_generator.make_token(account)
