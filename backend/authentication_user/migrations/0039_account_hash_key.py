# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-18 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0038_auto_20180710_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='hash_key',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
