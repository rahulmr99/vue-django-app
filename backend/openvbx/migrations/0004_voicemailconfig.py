# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-25 18:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0019_auto_20171111_1305'),
        ('openvbx', '0003_voicemail_recorded_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceMailConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('greeting_message', models.CharField(default='Hello. Please leave a message after the beep.', max_length=200)),
                ('use_audio', models.BooleanField(default=False)),
                ('greeting_voice', models.FileField(blank=True, null=True, upload_to='')),
                ('generalsettings', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings')),
            ],
        ),
    ]
