# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-14 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0004_account_is_customers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(default='', max_length=255, verbose_name='Username'),
        ),
    ]
