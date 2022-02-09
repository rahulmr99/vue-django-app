# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-11 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0019_auto_20171108_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='country',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='country_code',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
