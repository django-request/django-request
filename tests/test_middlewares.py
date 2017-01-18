# -*- coding: utf-8 -*-
from unittest import skipIf

import django
import mock
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from request.middleware import RequestMiddleware
from request.models import Request

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    # to keep backward (Django <= 1.4) compatibility
    from django.contrib.auth.models import User


class RequestMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestMiddleware()

    def test_record(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        self.middleware.process_response(request, response)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('django.conf.settings.MIDDLEWARE', [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'request.middleware.RequestMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ])
    @skipIf(django.VERSION < (1, 10), 'Django >= 1.10 specific test')
    def test_middleware_functions_supported(self):
        '''
        Test support of a middleware factory that was introduced in Django == 1.10
        '''
        request = self.factory.get('/foo')
        RequestMiddleware(request)

    @mock.patch('request.settings.VALID_METHOD_NAMES',
                ('get',))
    def test_dont_record_unvalid_method_name(self):
        request = self.factory.post('/foo')
        response = HttpResponse()
        self.middleware.process_response(request, response)
        self.assertEqual(0, Request.objects.count())

    @mock.patch('request.middleware.settings.VALID_METHOD_NAMES',
                ('get',))
    def test_record_valid_method_name(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        self.middleware.process_response(request, response)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.ONLY_ERRORS',
                False)
    def test_dont_record_only_error(self):
        request = self.factory.get('/foo')
        # Errored
        response = HttpResponse(status=500)
        self.middleware.process_response(request, response)
        # Succeed
        response = HttpResponse(status=200)
        self.middleware.process_response(request, response)

        self.assertEqual(2, Request.objects.count())

    @mock.patch('request.middleware.settings.ONLY_ERRORS',
                True)
    def test_record_only_error(self):
        request = self.factory.get('/foo')
        # Errored
        response = HttpResponse(status=500)
        self.middleware.process_response(request, response)
        # Succeed
        response = HttpResponse(status=200)
        self.middleware.process_response(request, response)

        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_PATHS',
                (r'^foo',))
    def test_dont_record_ignored_paths(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        # Ignored path
        self.middleware.process_response(request, response)
        # Recorded
        request = self.factory.get('/bar')
        self.middleware.process_response(request, response)

        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_AJAX',
                True)
    def test_dont_record_ajax(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        # Non-Ajax
        self.middleware.process_response(request, response)
        # Ajax
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.middleware.process_response(request, response)

        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_AJAX',
                False)
    def test_record_ajax(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        # Non-Ajax
        self.middleware.process_response(request, response)
        # Ajax
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.middleware.process_response(request, response)

        self.assertEqual(2, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_IP',
                ('1.2.3.4',))
    def test_dont_record_ignored_ips(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        # Ignored IP
        request.META['REMOTE_ADDR'] = '1.2.3.4'
        self.middleware.process_response(request, response)
        # Recorded
        request.META['REMOTE_ADDR'] = '5.6.7.8'
        self.middleware.process_response(request, response)

        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_USER_AGENTS',
                (r'^.*Foo.*$',))
    def test_dont_record_ignored_user_agents(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        # Ignored
        request.META['HTTP_USER_AGENT'] = 'Foo'
        self.middleware.process_response(request, response)
        request.META['HTTP_USER_AGENT'] = 'FooV2'
        self.middleware.process_response(request, response)
        # Recorded
        request.META['HTTP_USER_AGENT'] = 'Bar'
        self.middleware.process_response(request, response)
        request.META['HTTP_USER_AGENT'] = 'BarV2'
        self.middleware.process_response(request, response)

        self.assertEqual(2, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_USERNAME',
                ('foo',))
    def test_dont_record_ignored_user_names(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        # Anonymous
        self.middleware.process_response(request, response)
        # Ignored
        request.user = User.objects.create(username='foo')
        self.middleware.process_response(request, response)
        # Recorded
        request.user = User.objects.create(username='bar')
        self.middleware.process_response(request, response)

        self.assertEqual(2, Request.objects.count())
