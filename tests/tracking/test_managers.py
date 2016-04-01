from datetime import timedelta
from django.test import TestCase
from django.utils.timezone import now
from request.tracking.models import Visitor, Visit
from request.models import Request


class VisitorQuerySetTest(TestCase):
    def test_repeated(self):
        self.assertEqual(0, Visitor.objects.all().repeated().count())
        # 1st visit
        self.client.get('/admin/login/')
        self.assertEqual(0, Visitor.objects.all().repeated().count())
        # 2nd visit
        Request.objects.update(time=now()-timedelta(days=1))
        self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.all().repeated().count())

    def test_new(self):
        self.assertEqual(0, Visitor.objects.all().new().count())
        # 1st visit
        self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.all().new().count())
        # 2nd visit
        self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.all().new().count())
        # 3rd visit, new client
        self.client.cookies.pop('track_key')
        self.client.get('/admin/login/')
        self.assertEqual(2, Visitor.objects.all().new().count())

    def in_progress(self):
        self.assertEqual(0, Visitor.objects.all().in_progress().count())
        # 1st visit
        self.client.get('/admin/login/')
        self.assertEqual(1, Visitor.objects.all().in_progress().count())
        # 2nd visit, in_progress client
        self.client.cookies.pop('track_key')
        self.client.get('/admin/login/')
        self.assertEqual(2, Visitor.objects.all().in_progress().count())
        # Change request time and test
        Request.objects.update(time=now()-timedelta(days=1))
        self.assertEqual(0, Visitor.objects.all().in_progress().count())


class VisitorManagerTest(TestCase):
    pass


class VisitQuerySetTest(TestCase):
    def test_in_progress(self):
        self.assertEqual(0, Visit.objects.all().in_progress().count())
        # 1st visit
        self.client.get('/admin/login/')
        self.assertEqual(1, Visit.objects.all().in_progress().count())
        # 2nd visit, in_progress client
        self.client.cookies.pop('track_key')
        self.client.get('/admin/login/')
        self.assertEqual(2, Visit.objects.all().in_progress().count())
        # Change request time and test
        Request.objects.update(time=now()-timedelta(days=1))
        self.assertEqual(0, Visit.objects.all().in_progress().count())

    def test_singleton(self):
        self.assertEqual(0, Visit.objects.all().singleton().count())
        # 1st visit
        self.client.get('/admin/login/')
        self.assertEqual(1, Visit.objects.all().singleton().count())
        # 2nd visit
        self.client.get('/admin/login/')
        self.assertEqual(0, Visit.objects.all().singleton().count())
        # 3rd visit, new client
        self.client.cookies.pop('track_key')
        self.client.get('/admin/login/')
        self.assertEqual(1, Visit.objects.all().singleton().count())
        # 4rd visit, new client
        self.client.cookies.pop('track_key')
        self.client.get('/admin/login/')
        self.assertEqual(2, Visit.objects.all().singleton().count())
