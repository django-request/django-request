# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_auto_20160331_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('requests', models.ManyToManyField(to='request.Request')),
            ],
            options={
                'verbose_name': 'visit',
                'verbose_name_plural': 'visits',
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('requests', models.ManyToManyField(to='request.Request')),
            ],
            options={
                'verbose_name': 'visitor',
                'verbose_name_plural': 'visitors',
            },
        ),
        migrations.AddField(
            model_name='visit',
            name='visitor',
            field=models.ForeignKey(to='tracking.Visitor'),
        ),
    ]
