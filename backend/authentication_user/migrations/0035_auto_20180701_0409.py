# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-01 08:09
from __future__ import unicode_literals

import authentication_user.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0034_auto_20180625_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='mobile',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[authentication_user.validators.validate_phone_number], verbose_name='Telephone'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[authentication_user.validators.validate_phone_number], verbose_name='Mobile phone'),
        ),
    ]
