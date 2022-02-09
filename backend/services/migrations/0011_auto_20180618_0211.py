# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-18 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_auto_20180416_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Name'),
        ),
    ]
