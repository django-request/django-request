# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-13 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_alter_time_timezone_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='data',
            field=models.TextField(blank=True, null=True, verbose_name='data'),
        ),
        migrations.AddField(
            model_name='request',
            name='params',
            field=models.TextField(blank=True, null=True, verbose_name='params'),
        ),
    ]