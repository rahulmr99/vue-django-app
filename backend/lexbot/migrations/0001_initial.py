# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-18 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_settings', '0020_feedbackconfig_send_time_in_delta'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caller_number', models.CharField(db_index=True, max_length=20)),
                ('caller_country', models.CharField(db_index=True, max_length=50)),
                ('req_data', models.TextField()),
                ('generalsettings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings')),
            ],
        ),
    ]
