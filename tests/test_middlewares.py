import mock
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from request.middleware import RequestMiddleware
from request.models import Request

User = get_user_model()


class RequestMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestMiddleware()

    def test_record(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        self.middleware.process_response(request, response)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.settings.REQUEST_VALID_METHOD_NAMES',
                ('get',))
    def test_dont_record_unvalid_method_name(self):
        request = self.factory.post('/foo')
        response = HttpResponse()
        self.middleware.process_response(request, response)
        self.assertEqual(0, Request.objects.count())

    @mock.patch('request.middleware.settings.REQUEST_VALID_METHOD_NAMES',
                ('get',))
    def test_record_valid_method_name(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        self.middleware.process_response(request, response)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.REQUEST_ONLY_ERRORS',
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

    @mock.patch('request.middleware.settings.REQUEST_ONLY_ERRORS',
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

    @mock.patch('request.middleware.settings.REQUEST_IGNORE_PATHS',
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

    @mock.patch('request.middleware.settings.REQUEST_IGNORE_AJAX',
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

    @mock.patch('request.middleware.settings.REQUEST_IGNORE_AJAX',
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

    @mock.patch('request.middleware.settings.REQUEST_IGNORE_IP',
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

    @mock.patch('request.middleware.settings.REQUEST_IGNORE_USER_AGENTS',
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

    @mock.patch('request.middleware.settings.REQUEST_IGNORE_USERNAME',
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
