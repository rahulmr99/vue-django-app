# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_manager', '0004_auto_20170720_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendardb',
            name='uid',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]
