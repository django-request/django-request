# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('response', models.SmallIntegerField(verbose_name='response', default=200, choices=[(100, 'Continue'), (101, 'Switching Protocols'), (102, 'Processing (WebDAV)'), (200, 'OK'), (201, 'Created'), (202, 'Accepted'), (203, 'Non-Authoritative Information'), (204, 'No Content'), (205, 'Reset Content'), (206, 'Partial Content'), (207, 'Multi-Status (WebDAV)'), (300, 'Multiple Choices'), (301, 'Moved Permanently'), (302, 'Found'), (303, 'See Other'), (304, 'Not Modified'), (305, 'Use Proxy'), (306, 'Switch Proxy'), (307, 'Temporary Redirect'), (400, 'Bad Request'), (401, 'Unauthorized'), (402, 'Payment Required'), (403, 'Forbidden'), (404, 'Not Found'), (405, 'Method Not Allowed'), (406, 'Not Acceptable'), (407, 'Proxy Authentication Required'), (408, 'Request Timeout'), (409, 'Conflict'), (410, 'Gone'), (411, 'Length Required'), (412, 'Precondition Failed'), (413, 'Request Entity Too Large'), (414, 'Request-URI Too Long'), (415, 'Unsupported Media Type'), (416, 'Requested Range Not Satisfiable'), (417, 'Expectation Failed'), (418, "I'm a teapot"), (422, 'Unprocessable Entity (WebDAV)'), (423, 'Locked (WebDAV)'), (424, 'Failed Dependency (WebDAV)'), (425, 'Unordered Collection'), (426, 'Upgrade Required'), (449, 'Retry With'), (500, 'Internal Server Error'), (501, 'Not Implemented'), (502, 'Bad Gateway'), (503, 'Service Unavailable'), (504, 'Gateway Timeout'), (505, 'HTTP Version Not Supported'), (506, 'Variant Also Negotiates'), (507, 'Insufficient Storage (WebDAV)'), (509, 'Bandwidth Limit Exceeded'), (510, 'Not Extended')])),
                ('method', models.CharField(verbose_name='method', default='GET', max_length=7)),
                ('path', models.CharField(verbose_name='path', max_length=255)),
                ('time', models.DateTimeField(verbose_name='time', auto_now_add=True)),
                ('is_secure', models.BooleanField(verbose_name='is secure', default=False)),
                ('is_ajax', models.BooleanField(verbose_name='is ajax', help_text='Wheather this request was used via javascript.', default=False)),
                ('ip', models.IPAddressField(verbose_name='ip address')),
                ('referer', models.URLField(verbose_name='referer', max_length=255, blank=True, null=True)),
                ('user_agent', models.CharField(verbose_name='user agent', max_length=255, blank=True, null=True)),
                ('language', models.CharField(verbose_name='language', max_length=255, blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'request',
                'verbose_name_plural': 'requests',
                'ordering': ('-time',),
            },
            bases=(models.Model,),
        ),
    ]
