# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-10 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0037_auto_20180708_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='chargebee_customer_id',
            field=models.CharField(blank=True, max_length=25, null=True),
        )
    ]
