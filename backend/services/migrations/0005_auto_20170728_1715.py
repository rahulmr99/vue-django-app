# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-28 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20170728_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='attendants',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Attendants Number'),
        ),
    ]