# -*- coding: utf-8 -*-
import json

from django.contrib.admin import site
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from request.admin import RequestAdmin
from request.models import Request

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    # to keep backward (Django <= 1.4) compatibility
    from django.contrib.auth.models import User


class LookupAllowedTest(TestCase):
    def test_lookup_allowed(self):
        admin = RequestAdmin(Request, site)
        admin.lookup_allowed('user__username', 'foo')
        admin.lookup_allowed('response', 200)


class RequestFromTest(TestCase):
    def test_user_id(self):
        admin = RequestAdmin(Request, site)
        user = User.objects.create(username='foo')
        request = Request.objects.create(user=user, ip='1.2.3.4')
        admin.request_from(request)

    def test_without_user_id(self):
        admin = RequestAdmin(Request, site)
        request = Request.objects.create(ip='1.2.3.4')
        admin.request_from(request)


class GetUrlsTest(TestCase):
    def test_get_urls(self):
        admin = RequestAdmin(Request, site)
        admin.get_urls()


class OverviewTest(TestCase):
    def test_overview(self):
        admin = RequestAdmin(Request, site)
        factory = RequestFactory()
        request = factory.get('/foo')
        admin.overview(request)


class TrafficTest(TestCase):
    def setUp(self):
        self.admin = RequestAdmin(Request, site)
        self.factory = RequestFactory()

    def test_traffic(self):
        request = self.factory.get('/foo')
        self.admin.traffic(request)

    def test_bad_days(self):
        request = self.factory.get('/foo', {'days': 'foo'})
        self.admin.traffic(request)

    def test_days_lt_10(self):
        request = self.factory.get('/foo', {'days': 9})
        self.admin.traffic(request)

    def test_days_gt_60(self):
        request = self.factory.get('/foo', {'days': 61})
        self.admin.traffic(request)


class RequestAdminViewsTest(TestCase):
    def setUp(self):
        user = User(username='foo', is_superuser=True, is_staff=True)
        user.set_password('bar')
        user.save()
        self.client.login(username=user.username, password='bar')

    def test_overview(self):
        url = reverse('admin:request_request_overview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_traffic(self):
        url = reverse('admin:request_request_traffic')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertIsInstance(json_response, list)
        self.assertIsInstance(json_response[0], dict)
        self.assertIn('data', json_response[0])
        self.assertIn('label', json_response[0])
        for time, value in json_response[0]['data']:
            self.assertIsInstance(time, float)
            self.assertIsInstance(value, int)
