# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-21 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openvbx', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voicemail',
            name='transcription_text',
            field=models.TextField(default='Voice is being transcribed...'),
        ),
    ]