# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='ip',
            field=models.GenericIPAddressField(verbose_name='ip address'),
        ),
        migrations.AlterField(
            model_name='request',
            name='method',
            field=models.CharField(verbose_name='method', default='GET', max_length=7),
        ),
    ]
