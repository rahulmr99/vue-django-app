# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-11 18:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0018_emailsubscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailsubscription',
            name='account',
        ),
        migrations.RemoveField(
            model_name='emailsubscription',
            name='generalsettings',
        ),
        migrations.DeleteModel(
            name='EmailSubscription',
        ),
    ]
