# -*- coding: utf-8 -*-
from datetime import timedelta

import mock
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.timezone import now
from request.management.commands.purgerequests import Command as PurgeRequest
from request.management.commands.purgerequests import DURATION_OPTIONS
from request.models import Request


class PurgeRequestsTest(TestCase):
    def setUp(self):
        Request.objects.create(ip='1.2.3.4')
        request = Request.objects.create(ip='1.2.3.4')
        request.time = now() - timedelta(days=31)
        request.save()

    def test_duration_options(self, *mock):
        for opt, func in DURATION_OPTIONS.items():
            self.assertLess(func(10), now())

    @mock.patch('request.management.commands.purgerequests.input',
                return_value='yes')
    def test_purge_requests(self, *mock):
        PurgeRequest().handle(amount=1, duration='days')
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.management.commands.purgerequests.input',
                return_value='yes')
    def test_duration_without_s(self, *mock):
        PurgeRequest().handle(amount=1, duration='day')
        self.assertEqual(1, Request.objects.count())

    def test_invalid_duration(self, *mock):
        with self.assertRaises(CommandError):
            PurgeRequest().handle(amount=1, duration='foo')
        self.assertEqual(2, Request.objects.count())

    def test_no_request_to_delete(self, *mock):
        PurgeRequest().handle(amount=1, duration='days')

    @mock.patch('request.management.commands.purgerequests.input',
                return_value='no')
    def test_interactive_non_confirmed(self, *mock):
        PurgeRequest().handle(amount=1, duration='days', interactive=True)
        self.assertTrue(mock[0].called)
        self.assertEqual(2, Request.objects.count())

    @mock.patch('request.management.commands.purgerequests.input',
                return_value='yes')
    def test_non_interactive(self, *mock):
        PurgeRequest().handle(amount=1, duration='days', interactive=False)
        self.assertFalse(mock[0].called)
        self.assertEqual(1, Request.objects.count())
