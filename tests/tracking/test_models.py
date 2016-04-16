from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from request.models import Request
from request.tracking.models import Visit, Visitor


class VisitorModelTest(TestCase):
    def test_str(self):
        visitor = Visitor.objects.create(key='foo')
        visitor.__str__()

    def test_no_first_time(self):
        visitor = Visitor.objects.create(key='foo')
        self.assertIsNone(visitor.first_time())

    def test_first_time(self):
        self.client.get('/admin/login/')
        request = Request.objects.first()
        visitor = Visitor.objects.first()
        self.assertEqual(request.time, visitor.first_time())
        # 2nd request
        self.client.get('/admin/login/')
        self.assertEqual(request.time, visitor.first_time())

    def test_no_last_time(self):
        visitor = Visitor.objects.create(key='foo')
        self.assertIsNone(visitor.first_time())

    def test_last_time(self):
        self.client.get('/admin/login/')
        request = Request.objects.first()
        visitor = Visitor.objects.first()
        self.assertEqual(request.time, visitor.last_time())
        # 2nd request
        self.client.get('/admin/login/')
        request = Request.objects.order_by('-time').first()
        self.assertEqual(request.time, visitor.last_time())

    def test_recency(self):
        self.skipTest("Not implemented")

    def test_in_progress(self):
        self.client.get('/admin/login/')
        visitor = Visitor.objects.first()
        self.assertTrue(visitor.in_progress())
        # Change request time and test
        Request.objects.update(time=now()-timedelta(days=1))
        self.assertFalse(visitor.in_progress())


class VisitModelTest(TestCase):
    def test_str(self):
        visit = Visit.objects.create(visitor=Visitor.objects.create(key='foo'))
        visit.__str__()

    def test_no_first_time(self):
        visit = Visit.objects.create(visitor=Visitor.objects.create(key='foo'))
        self.assertIsNone(visit.first_time())

    def test_first_time(self):
        self.client.get('/admin/login/')
        request = Request.objects.first()
        visit = Visit.objects.first()
        self.assertEqual(request.time, visit.first_time())
        # 2nd request
        self.client.get('/admin/login/')
        self.assertEqual(request.time, visit.first_time())

    def test_no_last_time(self):
        visit = Visit.objects.create(visitor=Visitor.objects.create(key='foo'))
        self.assertIsNone(visit.last_time())

    def test_last_time(self):
        self.client.get('/admin/login/')
        request = Request.objects.first()
        visit = Visit.objects.first()
        self.assertEqual(request.time, visit.last_time())
        # 2nd request
        self.client.get('/admin/login/')
        request = Request.objects.order_by('-time').first()
        self.assertEqual(request.time, visit.last_time())

    def test_in_progress(self):
        self.client.get('/admin/login/')
        visit = Visit.objects.first()
        self.assertTrue(visit.in_progress())
        # Change request time and test
        Request.objects.update(time=now()-timedelta(days=1))
        self.assertFalse(visit.in_progress())
