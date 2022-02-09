# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-29 11:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_datetime', models.DateTimeField()),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('is_unavailable', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
                ('services', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.Service')),
                ('users_customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.Customers')),
                ('users_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User provider')),
            ],
            options={
                'verbose_name': '1. Calendar',
                'ordering': ['-id', '-book_datetime'],
            },
        ),
    ]