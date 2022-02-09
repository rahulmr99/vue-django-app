# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-11 08:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0011_create_initial_settings'),
        ('services', '0006_auto_20170808_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='generalsettings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='generalsettings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings'),
            preserve_default=False,
        ),
    ]
