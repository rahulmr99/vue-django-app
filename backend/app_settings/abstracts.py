from django.db import models
from django_extensions.db.models import TimeStampedModel

from app_settings.utils import get_email_template


class AbstractEmailModel(TimeStampedModel):
    # model fields
    generalsettings = models.OneToOneField('app_settings.GeneralSettings', on_delete=models.CASCADE)
    email_subject = models.CharField(max_length=500)
    email_body = models.TextField()

    # attrs
    default_email_template_name = None
    default_email_subject = None

    class Meta:
        abstract = True

    def set_defaults(self):
        self.email_body = get_email_template(type(self).default_email_template_name)
        self.email_subject = type(self).default_email_subject

    @classmethod
    def create_for(cls, generalsettings_id):
        obj = cls()
        obj.set_defaults()
        obj.generalsettings_id = generalsettings_id
        obj.save()
        return obj
