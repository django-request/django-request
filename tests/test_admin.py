import json
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.admin import site
from request.admin import RequestAdmin
from request.models import Request

User = get_user_model()


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
        html = admin.request_from(request)

    def test_without_user_id(self):
        admin = RequestAdmin(Request, site)
        request = Request.objects.create(ip='1.2.3.4')
        html = admin.request_from(request)


class GetUrlsTest(TestCase):
    def test_get_urls(self):
        admin = RequestAdmin(Request, site)
        urls = admin.get_urls()


class OverviewTest(TestCase):
    def test_overview(self):
        admin = RequestAdmin(Request, site)
        factory = RequestFactory()
        request = factory.get('/foo')
        response = admin.overview(request)


class TrafficTest(TestCase):
    def setUp(self):
        self.admin = RequestAdmin(Request, site)
        self.factory = RequestFactory()

    def test_traffic(self):
        request = self.factory.get('/foo')
        response = self.admin.traffic(request)

    def test_bad_days(self):
        request = self.factory.get('/foo', {'days': 'foo'})
        response = self.admin.traffic(request)

    def test_days_lt_10(self):
        request = self.factory.get('/foo', {'days': 9})
        response = self.admin.traffic(request)

    def test_days_gt_60(self):
        request = self.factory.get('/foo', {'days': 61})
        response = self.admin.traffic(request)


class RequestAdminViewsTest(TestCase):
    def setUp(self):
        user = User(username='foo', is_superuser=True, is_staff=True)
        user.set_password('bar')
        user.save()
        self.client.login(username=user.username, password='bar')

    def test_overview(self):
        # TODO: Don't work
        # url = reverse('request_request_overview')
        url = '/admin/request/request/overview/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_traffic(self):
        # TODO: Don't work
        # url = reverse('request_request_traffic')
        url = '/admin/request/request/overview/traffic.json'
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
