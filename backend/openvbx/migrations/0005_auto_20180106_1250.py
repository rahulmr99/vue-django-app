# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-06 17:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openvbx', '0004_voicemailconfig'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='voicemailconfig',
            options={'ordering': ['-id']},
        ),
    ]
