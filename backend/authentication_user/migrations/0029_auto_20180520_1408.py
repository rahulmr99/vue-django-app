# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-20 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0028_auto_20180426_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
