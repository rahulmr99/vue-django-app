# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-16 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20180415_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Category', verbose_name='Category'),
        ),
    ]
