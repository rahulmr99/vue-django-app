# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-25 05:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_user', '0033_account_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='timezone',
            field=models.CharField(choices=[('US/Alaska', 'US/Alaska'), ('US/Arizona', 'US/Arizona'), ('US/Central', 'US/Central'), ('US/Eastern', 'US/Eastern'), ('US/Hawaii', 'US/Hawaii'), ('US/Mountain', 'US/Mountain'), ('US/Pacific', 'US/Pacific'), ('UTC', 'UTC'), ('EST', 'EST')], default='EST', max_length=80),
        ),
    ]