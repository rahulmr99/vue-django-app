# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-22 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexbot', '0005_create_voicebot_config_for_existing_records'),
    ]

    operations = [
        migrations.AddField(
            model_name='voicebotconfig',
            name='redirect_telephone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='voicebotconfig',
            name='redirect_to_browser',
            field=models.BooleanField(default=True),
        ),
    ]
