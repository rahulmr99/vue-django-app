import os
import re

from django.contrib.sites.models import Site
from django.urls import reverse
from django.conf import settings

RE_CONTENT = re.compile(r"{%\s+block content.+endblock content\s+%}")

EMAIL_TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '..', 'mailer/templates', 'email')


def get_email_template(name):
    with open(os.path.join(EMAIL_TEMPLATES_PATH, f'base.html')) as f:
        template_str = f.read()
    with open(os.path.join(EMAIL_TEMPLATES_PATH, f'{name}.html')) as f:
        content = f.read()
        template_str = RE_CONTENT.sub(content, template_str)

    return template_str


def reverse_fullurl(url='', *args, **kwargs):
    """
        reverse and return a full qualified url. 
    Args:
        url: If the urlname is empty then returns just the domain name
        *args: arguments as you would pass to reverse's args
        **kwargs: kwargs as you would pass to reverse's kwargs

    Returns:
        str: full qualified URL
    """
    json = kwargs.pop('json', False)
    domain = str(Site.objects.get_current().domain)
    domain = domain.rstrip('/')
    if domain == 'example.com':
        domain = settings.BASE_DOMAIN_NAME

    return (
            domain
            + (reverse(url, args=args, kwargs=kwargs) if url else '')
            + ("?format=json" if json else ""))
