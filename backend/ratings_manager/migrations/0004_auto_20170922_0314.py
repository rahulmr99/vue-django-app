# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-22 07:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings_manager', '0003_auto_20170922_0222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='calendar',
            new_name='calendardb',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='user',
        ),
    ]
