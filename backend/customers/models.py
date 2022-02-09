from django.db import models


class Customers(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(blank=True, max_length=255, verbose_name='Last name')
    email = models.EmailField(blank=True, null=True, max_length=255, verbose_name='Email')
    phone = models.CharField(blank=True, null=True, max_length=255, verbose_name='Phone')
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name='Address')
    city = models.CharField(blank=True, null=True, max_length=255, verbose_name='City')
    zip_code = models.CharField(blank=True, null=True, max_length=255, verbose_name='Zip code')
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name='Note')

    def __str__(self):
        return f'[ Customer {self.first_name} {self.last_name} - {self.email}]'

    class Meta:
        verbose_name = '1. Customers'
        ordering = ['-id', ]
