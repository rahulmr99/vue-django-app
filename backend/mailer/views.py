from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView
from itsdangerous import URLSafeSerializer
from utils_plus.utils import reverse_url

from authentication_user.choices import MAIL_STATUS
from mailer.forms import ConfirmUnsubscribeForm

SIGNER = URLSafeSerializer(settings.SECRET_KEY)


@method_decorator(csrf_exempt, name='dispatch')
class ConfirmUnsubscribeView(FormView):
    """user clicked to unsubscribe and show them a confirmation page to ensure their action"""
    form_class = ConfirmUnsubscribeForm
    template_name = 'mailer/confirm-unsubscribe.html'

    def get_success_url(self):
        return reverse_url('mailer:notify-unsubscribed', self.kwargs['mailid_encoded'])

    def form_valid(self, form):
        from authentication_user.models import Account
        mailid = SIGNER.loads(self.kwargs['mailid_encoded'])
        account = get_object_or_404(Account, email=mailid)
        account.email_subscription_status = MAIL_STATUS.unsubscribed.name
        account.save()
        return super(ConfirmUnsubscribeView, self).form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class ShowUnsubscribedView(TemplateView):
    """
        after confirming the unsubscription show confirmation page.
    Args:
        request:

    Returns:

    """
    template_name = 'mailer/unsubscribed.html'
