# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-06 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_manager', '0002_auto_20170706_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendardb',
            name='book_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
