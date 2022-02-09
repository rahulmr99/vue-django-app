# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-19 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_manager', '0010_calendardb_google_calendar_event_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendardb',
            name='generalsettings',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings'),
            preserve_default=False,
        ),
    ]