# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-08 07:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rasa_bot', '0002_rasabotusersession_activity_track'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rasabotusersession',
            name='activity_track',
        ),
    ]
