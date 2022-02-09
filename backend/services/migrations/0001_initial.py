# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-29 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='Duration')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price')),
                ('currency', models.SmallIntegerField(choices=[(2, 'EUR'), (1, 'USD')], default=1, verbose_name='Currency')),
                ('category', models.SmallIntegerField(choices=[(2, 'Test 2'), (1, 'Test 1')], default=1, verbose_name='Category')),
                ('availabilities_type', models.SmallIntegerField(choices=[(2, 'Test 2'), (1, 'Test 1')], default=1, verbose_name='Availabilities Type')),
                ('attendants', models.PositiveIntegerField(default=1, verbose_name='Attendants Number')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': '1. Service',
                'ordering': ['-id'],
            },
        ),
    ]