import unittest
from datetime import datetime
from django.conf import settings
settings.configure()
from django.http import HttpRequest, HttpResponse
from request.models import Request


class RequestTests(unittest.TestCase):
    def test_from_http_request(self):
        http_request = HttpRequest()
        http_request.method = 'PATCH'
        http_request.path = '/kylef'
        http_request.META['REMOTE_ADDR'] = '32.64.128.16'

        http_response = HttpResponse(status=204)

        request = Request()
        request.from_http_request(http_request, http_response, commit=False)

        self.assertEqual(request.path, '/kylef')
        self.assertEqual(request.method, 'PATCH')
        self.assertEqual(request.ip, '32.64.128.16')
        self.assertEqual(request.response, 204)

    def test_unicode(self):
        request = Request(method='PATCH', path='/', response=204)
        request.time = datetime.now()
        self.assertEqual(unicode(request), '[{}] PATCH / 204'.format(request.time))
