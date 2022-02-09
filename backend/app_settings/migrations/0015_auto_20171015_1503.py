# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-15 19:03
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0014_auto_20171013_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalsettings',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['company_name', 'company_link', 'id'], unique=True),
        ),
    ]
