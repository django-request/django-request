from datetime import timedelta

from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils.timezone import now

from request.middleware import RequestMiddleware
from request.models import Request
from request.tracking.models import Visit, Visitor


class RequestMiddlewareWithTrackingTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestMiddleware()

    def test_record(self):
        request = self.factory.get('/foo')
        response = HttpResponse()
        response = self.middleware.process_response(request, response)
        self.assertTrue(Visitor.objects.exists())
        self.assertTrue(Visit.objects.exists())
        self.assertIn('track_key', response.cookies)


class VisitorRecordTest(TestCase):
    def test_record_visit(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(1, Request.objects.count())
        self.assertEqual(1, Visitor.objects.count())
        self.assertEqual(1, Visit.objects.count())
        request = Request.objects.get()
        self.assertEqual(1, request.visitor_set.count())
        self.assertEqual(1, request.visit_set.count())

    def test_client_drop_cookie(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.count())
        self.assertEqual(1, Visit.objects.count())
        # 2nd request with cookie
        response = self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.count())
        self.assertEqual(1, Visit.objects.count())
        # 3rd request with new client
        self.client.cookies.pop('track_key')
        response = self.client.get('/admin/login/')
        self.assertEqual(2, Visitor.objects.count())
        self.assertEqual(2, Visit.objects.count())

    def test_visit_timeout(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.count())
        self.assertEqual(1, Visit.objects.count())
        # Change request to older time
        Request.objects.update(time=now()-timedelta(days=1))
        response = self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.count())
        self.assertEqual(2, Visit.objects.count())
