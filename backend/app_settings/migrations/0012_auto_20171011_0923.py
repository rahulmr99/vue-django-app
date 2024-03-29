# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-11 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0011_create_initial_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackconfig',
            name='generalsettings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='initialconfirmation',
            name='generalsettings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reminder',
            name='generalsettings',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings'),
            preserve_default=False,
        ),
    ]
