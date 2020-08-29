import mock
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseServerError
from django.test import RequestFactory, TestCase

from request.middleware import RequestMiddleware
from request.models import Request


def get_response_empty(request):
    return HttpResponse()


def get_response_server_error(request):
    return HttpResponseServerError()


class RequestMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestMiddleware(get_response_empty)

    def test_record(self):
        request = self.factory.get('/foo')
        self.middleware(request)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('django.conf.settings.MIDDLEWARE', [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'request.middleware.RequestMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ])
    def test_middleware_functions_supported(self):
        request = self.factory.get('/foo')
        RequestMiddleware(request)

    @mock.patch('request.settings.VALID_METHOD_NAMES',
                ('get',))
    def test_dont_record_unvalid_method_name(self):
        request = self.factory.post('/foo')
        self.middleware(request)
        self.assertEqual(0, Request.objects.count())

    @mock.patch('request.middleware.settings.VALID_METHOD_NAMES',
                ('get',))
    def test_record_valid_method_name(self):
        request = self.factory.get('/foo')
        self.middleware(request)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.ONLY_ERRORS',
                False)
    def test_dont_record_only_error(self):
        request = self.factory.get('/foo')
        # Errored
        RequestMiddleware(get_response_server_error)(request)
        # Succeed
        self.middleware(request)
        self.assertEqual(2, Request.objects.count())

    @mock.patch('request.middleware.settings.ONLY_ERRORS',
                True)
    def test_record_only_error(self):
        request = self.factory.get('/foo')
        # Errored
        RequestMiddleware(get_response_server_error)(request)
        # Succeed
        self.middleware(request)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_PATHS',
                (r'^foo',))
    def test_dont_record_ignored_paths(self):
        request = self.factory.get('/foo')
        # Ignored path
        self.middleware(request)
        # Recorded
        request = self.factory.get('/bar')
        self.middleware(request)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_AJAX',
                True)
    def test_dont_record_ajax(self):
        request = self.factory.get('/foo')
        # Non-Ajax
        self.middleware(request)
        # Ajax
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.middleware(request)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_AJAX',
                False)
    def test_record_ajax(self):
        request = self.factory.get('/foo')
        # Non-Ajax
        self.middleware(request)
        # Ajax
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.middleware(request)
        self.assertEqual(2, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_IP',
                ('1.2.3.4',))
    def test_dont_record_ignored_ips(self):
        request = self.factory.get('/foo')
        # Ignored IP
        request.META['REMOTE_ADDR'] = '1.2.3.4'
        self.middleware(request)
        # Recorded
        request.META['REMOTE_ADDR'] = '5.6.7.8'
        self.middleware(request)
        self.assertEqual(1, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_USER_AGENTS',
                (r'^.*Foo.*$',))
    def test_dont_record_ignored_user_agents(self):
        request = self.factory.get('/foo')
        # Ignored
        request.META['HTTP_USER_AGENT'] = 'Foo'
        self.middleware(request)
        request.META['HTTP_USER_AGENT'] = 'FooV2'
        self.middleware(request)
        # Recorded
        request.META['HTTP_USER_AGENT'] = 'Bar'
        self.middleware(request)
        request.META['HTTP_USER_AGENT'] = 'BarV2'
        self.middleware(request)
        self.assertEqual(2, Request.objects.count())

    @mock.patch('request.middleware.settings.IGNORE_USERNAME',
                ('foo',))
    def test_dont_record_ignored_user_names(self):
        request = self.factory.get('/foo')
        # Anonymous
        self.middleware(request)
        # Ignored
        request.user = get_user_model().objects.create(username='foo')
        self.middleware(request)
        # Recorded
        request.user = get_user_model().objects.create(username='bar')
        self.middleware(request)
        self.assertEqual(2, Request.objects.count())
