# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-29 09:49
from __future__ import unicode_literals

from django.db import migrations

from app_settings.utils import get_email_template


def create(apps, schema_editor):
    print('no longer needed to run this')

def down(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('app_settings', '0010_auto_20170928_0856'),
    ]

    operations = [
        migrations.RunPython(create, down),
    ]
