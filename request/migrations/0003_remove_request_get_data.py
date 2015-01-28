# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0002_auto_20150128_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='get_data',
        ),
    ]
