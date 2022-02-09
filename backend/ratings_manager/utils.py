from authentication_user.models import SIGNER
from calendar_manager.models import CalendarDb, SALT


def decode_calendar(sign: str):
    """
        from the token and id returns the user object if they are valid
    Args:
        sign: signed value
        token:

    Returns:
        Union[CalendarDb, None]:
    """

    try:
        pk = SIGNER.loads(sign, salt=SALT)
        return CalendarDb.objects.get(pk=pk)
    except:
        pass
