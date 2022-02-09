# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-22 20:16
from __future__ import unicode_literals

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_manager', '0016_calendardb_old_start_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendardb',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='calendardb',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
