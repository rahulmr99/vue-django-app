# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-10-26 07:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lexbot', '0014_callerinfoqueue_provider_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callerinfoqueue',
            name='generalsettings',
        ),
        migrations.DeleteModel(
            name='CallerInfoQueue',
        ),
    ]