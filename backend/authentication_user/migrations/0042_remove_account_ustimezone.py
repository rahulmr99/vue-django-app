# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-31 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0041_account_ustimezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='usTimeZone',
        ),
    ]
