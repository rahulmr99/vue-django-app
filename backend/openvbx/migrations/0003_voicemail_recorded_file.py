# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-25 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openvbx', '0002_auto_20171221_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='voicemail',
            name='recorded_file',
            field=models.FileField(blank=True, null=True, upload_to='voicemails/%Y/%m/%d/'),
        ),
    ]
