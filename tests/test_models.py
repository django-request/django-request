import socket
from datetime import datetime

import mock
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from request import settings
from request.models import Request


class RequestTests(TestCase):
    def test_from_http_request(self):
        http_request = HttpRequest()
        http_request.method = 'PATCH'
        http_request.path = '/kylef'
        http_request.META['REMOTE_ADDR'] = '32.64.128.16'
        http_request.META['HTTP_USER_AGENT'] = 'test user agent'
        http_request.META['HTTP_REFERER'] = 'https://fuller.li/'

        http_response = HttpResponse(status=204)

        request = Request()
        request.from_http_request(http_request, http_response, commit=False)

        self.assertEqual(request.path, '/kylef')
        self.assertEqual(request.method, 'PATCH')
        self.assertEqual(request.ip, '32.64.128.16')
        self.assertEqual(request.response, 204)
        self.assertEqual(request.user_agent, 'test user agent')
        self.assertEqual(request.referer, 'https://fuller.li/')

    def test_from_http_request_with_user(self):
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.user = get_user_model().objects.create(username='foo')

        request = Request()
        request.from_http_request(http_request, commit=False)
        self.assertEqual(request.user.id, http_request.user.id)

    def test_from_http_request_redirection(self):
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_response = HttpResponse(status=301)
        http_response['Location'] = '/foo'

        request = Request()
        request.from_http_request(http_request, http_response, commit=False)
        self.assertEqual(request.redirect, '/foo')

    def test_from_http_request_not_commit(self):
        http_request = HttpRequest()
        http_request.method = 'GET'

        request = Request()
        request.from_http_request(http_request, commit=False)
        self.assertIsNone(request.id)

    def test_str_conversion(self):
        request = Request(method='PATCH', path='/', response=204)
        request.time = datetime.now()
        self.assertEqual(str(request), '[{}] PATCH / 204'.format(request.time))

    def test_browser_detection_with_no_ua(self):
        request = Request(method='GET', path='/', response=200)
        self.assertEqual(request.browser, None)

    def test_browser_detection_with_no_path(self):
        request = Request(user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0')
        self.assertEqual(request.browser, 'Firefox')
        request = Request(user_agent='Mozilla/5.0 (compatible; MSIE 9.0; America Online Browser 1.1; Windows NT 5.0)')
        self.assertEqual(request.browser, 'AOL')

    def test_determining_search_keywords_with_no_referer(self):
        request = Request()
        self.assertEqual(request.keywords, None)

    def test_determining_search_keywords(self):
        request = Request(
            referer='https://www.google.com/search?client=safari&rls=en&q=querykit+core+data&ie=UTF-8&oe=UTF-8'
        )
        self.assertEqual(request.keywords, 'querykit core data')

    @mock.patch('request.models.gethostbyaddr',
                return_value=('foo.net', [], ['1.2.3.4']))
    def test_hostname(self, *mocks):
        request = Request(ip='1.2.3.4')
        self.assertEqual(request.hostname, 'foo.net')

    @mock.patch('request.models.gethostbyaddr',
                side_effect=socket.herror(2, 'Host name lookup failure'))
    def test_hostname_invalid(self, *mocks):
        request = Request(ip='1.2.3.4')
        self.assertEqual(request.hostname, request.ip)

    def test_save(self):
        request = Request(ip='1.2.3.4')
        request.save()

    @mock.patch('request.models.request_settings.LOG_IP',
                False)
    def test_save_not_log_ip(self):
        request = Request(ip='1.2.3.4')
        request.save()
        self.assertEqual(settings.IP_DUMMY, request.ip)

    @mock.patch('request.models.request_settings.ANONYMOUS_IP',
                True)
    def test_save_anonymous_ip(self):
        request = Request(ip='1.2.3.4')
        request.save()
        self.assertTrue(request.ip.endswith('.1'))

    @mock.patch('request.models.request_settings.LOG_USER',
                False)
    def test_save_not_log_user(self):
        user = get_user_model().objects.create(username='foo')
        request = Request(ip='1.2.3.4', user=user)
        request.save()
        self.assertIsNone(request.user)

    def test_get_user(self):
        user = get_user_model().objects.create(username='foo')
        request = Request.objects.create(ip='1.2.3.4', user=user)
        self.assertEqual(request.get_user(), user)
