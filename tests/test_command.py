from datetime import timedelta
from io import StringIO

import mock
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.timezone import now

from request.management.commands.purgerequests import DURATION_OPTIONS
from request.management.commands.purgerequests import Command as PurgeRequest
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

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_no_request_to_delete(self, mock_stdout):
        Request.objects.all().delete()
        PurgeRequest().handle(amount=1, duration='day', interactive=False)
        self.assertIn('There are no requests to delete.', mock_stdout.getvalue())

    @mock.patch('request.management.commands.purgerequests.input',
                return_value='no')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_interactive_non_confirmed(self, mock_stdout, mock_input):
        PurgeRequest().handle(amount=1, duration='days', interactive=True)
        self.assertTrue(mock_input.called)
        self.assertEqual(2, Request.objects.count())
        self.assertEqual('Purge cancelled\n', mock_stdout.getvalue())

    @mock.patch('request.management.commands.purgerequests.input',
                return_value='yes')
    def test_non_interactive(self, *mock):
        PurgeRequest().handle(amount=1, duration='days', interactive=False)
        self.assertFalse(mock[0].called)
        self.assertEqual(1, Request.objects.count())
