# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-23 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0023_auto_20180423_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancellationSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('email_subject', models.CharField(max_length=500)),
                ('email_body', models.TextField()),
                ('generalsettings', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReschedulingSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('email_subject', models.CharField(max_length=500)),
                ('email_body', models.TextField()),
                ('generalsettings', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_settings.GeneralSettings')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
