# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-29 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Last name')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('zip_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Zip code')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Note')),
            ],
            options={
                'verbose_name': '1. Customers',
                'ordering': ['-id'],
            },
        ),
    ]
