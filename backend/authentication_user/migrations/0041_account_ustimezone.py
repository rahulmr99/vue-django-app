# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-30 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0040_remove_account_hash_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='usTimeZone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
