# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-03 05:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings_manager', '0004_auto_20170922_0314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ['-id']},
        ),
    ]