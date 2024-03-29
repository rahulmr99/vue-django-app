# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 12:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_settings', '0003_initialconfirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_subject', models.CharField(max_length=500)),
                ('email_body', models.TextField()),
                ('send', models.BooleanField(default=True)),
                ('send_time', models.PositiveSmallIntegerField(default=24)),
                ('send_type', models.PositiveSmallIntegerField(choices=[(2, 'Client and Admin'), (1, 'Client')], default=1)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': '5. Reminder',
                'ordering': ['-id'],
            },
        ),
    ]
