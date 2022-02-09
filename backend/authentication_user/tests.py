from rest_framework.test import APIClient
from utils_plus.utils import reverse_url


def test_confirmation_code_model(db):
    from authentication_user.models import ConfirmationCode
    mail_id = 'root@gmail.com'
    code = ConfirmationCode.generate_confirm_code(mail_id)

    assert ConfirmationCode.objects.count() == 1
    assert ConfirmationCode.validate_confirmation_code(code, mail_id)
    assert ConfirmationCode.objects.count() == 0


def test_sending_reset_email(root_user, mailoutbox):
    apiclient = APIClient()
    resp: dict = apiclient.post(
        str(reverse_url('send_reset_link')),
        dict(email=root_user.email), format='json'
    ).data
    assert len(mailoutbox) == 1
