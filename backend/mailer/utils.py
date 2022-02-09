from django.template import Template, loader, Context
from typing import Union

from app_settings.utils import reverse_fullurl
from mailer.tasks import send_html_mail
from mailer.views import SIGNER


def send_mail_from_template_str(subject: str, template_context: dict, template: str, to_emails, from_name=None):
    """send emails where it gets template as a string form model"""
    send_mail_from_template(subject, Context(template_context), Template(template), to_emails, from_name)


def send_mail_using_template_name(subject: str, template_context: dict, template_name: str, to_emails, from_name=None):
    """find template from the given and send HTML email generated from that."""
    send_mail_from_template(subject, template_context, loader.get_template(template_name), to_emails, from_name)


def send_mail_from_template(
        subject: str,
        template_context: Union[Context, dict],
        template: Template,
        to_emails: str,
        from_name=None
):
    email_encoded = SIGNER.dumps(to_emails)
    template_context.update(
        {'unsubscribe_link': reverse_fullurl('mailer:confirm-unsubscribe', email_encoded)}
    )
    html_content = template.render(template_context)
    send_html_mail(subject, html_content, to_emails, from_name)
