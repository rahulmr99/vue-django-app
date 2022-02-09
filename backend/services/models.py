from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

from app_settings.models import GeneralSettings
from authentication_user.models import Account


class Service(models.Model):
    TYPE_CURRENCY = (
        (2, 'EUR'),
        (1, 'USD'),
    )
    TYPE_CATEGORY = (
        (2, 'Test 2'),
        (1, 'Test 1'),
    )
    TYPE_AVAILABILITIES = (
        (2, 'Fixed'),
        (1, 'Flexible'),
    )
    DEFAULT_DURATION = 30

    generalsettings = models.ForeignKey(GeneralSettings, on_delete=models.CASCADE, )
    name = models.CharField(max_length=255, verbose_name='Name', db_index=True)
    duration = models.PositiveIntegerField(verbose_name='Duration')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price')
    currency = models.SmallIntegerField(choices=TYPE_CURRENCY, default=1, blank=True, verbose_name='Currency')
    category = models.ForeignKey('Category', blank=True, null=True, verbose_name='Category',
                                 on_delete=models.SET_NULL, )
    availabilities_type = models.SmallIntegerField(choices=TYPE_CATEGORY, default=1, verbose_name='Availabilities Type')
    attendants = models.PositiveIntegerField(default=0, blank=True, verbose_name='Attendants Number')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    is_default = models.BooleanField(default=False)
    '''if True, then the service can't be deleted from the client applications'''

    def __str__(self):
        return f'[ Service {self.name} {self.duration} - {self.currency}]'

    class Meta:
        verbose_name = '1. Service'
        ordering = ['-id', ]

    @classmethod
    def create_default_services(cls, account: Account):
        if not account.is_provider:
            raise ValidationError({'provider': 'The account should be a provider account.'})
        for name in ['New Patient', 'Returning Patient', ]:
            attrs = dict(
                generalsettings_id=account.generalsettings_id, name=name, duration=cls.DEFAULT_DURATION, price=30,
            )
            service: Service = cls.objects.filter(**attrs).first()
            if not service:
                service = cls.objects.create(**attrs, is_default=True)
            elif not service.is_default:
                service.is_default = True
                service.save()
            if not account.services.filter(name=name).exists():
                account.services.add(service)

    @cached_property
    def provider(self) -> Account:
        return Account.objects.filter(
            generalsettings_id=self.generalsettings_id, is_provider=True,
            is_root_user=True
        ).first()

    def delete(self, **kw):
        if self.is_default:
            raise ValidationError("Can't delete one of default services")
        super(Service, self).delete(**kw)


class Category(models.Model):
    generalsettings = models.ForeignKey(GeneralSettings, on_delete=models.CASCADE, )
    name = models.CharField(max_length=255, verbose_name='Name')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return '[ Category {} - {}]'.format(self.name, self.description)

    class Meta:
        verbose_name = '2. Category'
        ordering = ['-id', ]
