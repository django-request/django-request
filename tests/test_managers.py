from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils.timezone import now

from request import settings
from request.managers import QUERYSET_PROXY_METHODS, RequestQuerySet
from request.models import Request


class RequestManagerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='foo')
        self.user_2 = get_user_model().objects.create(username='bar')

    def test_getattr(self):
        for meth in QUERYSET_PROXY_METHODS:
            Request.objects.__getattr__(meth)

    def test_getattr_not_in_proxy_methods(self):
        for meth in ('foo', 'bar'):
            self.assertRaises(AttributeError, Request.objects.__getattr__, meth)

    def test_get_queryset(self):
        queryset = Request.objects.get_queryset()
        self.assertIsInstance(queryset, RequestQuerySet)

    def test_active_users(self):
        Request.objects.create(user=self.user, ip='1.2.3.4')
        users = Request.objects.active_users()
        self.assertEqual(len(users), 1)

    def test_active_users_with_options(self):
        request = Request.objects.create(user=self.user, ip='1.2.3.4')
        request.time = now() - timedelta(days=1)
        request.save()
        options = {'minutes': 1, 'hours': 1}
        users = Request.objects.active_users(**options)
        self.assertEqual(len(users), 0)
        options = {'hours': 1, 'days': 1}
        users = Request.objects.active_users(**options)
        self.assertEqual(len(users), 1)

    @override_settings(USE_TZ=True, TIME_ZONE='Africa/Nairobi')
    def test_active_users_with_options_and_tz(self):
        request = Request.objects.create(user=self.user, ip='1.2.3.4')
        request.time = now() - timedelta(hours=1)
        request.save()
        options = {'minutes': 50, 'seconds': 20}
        users = Request.objects.active_users(**options)
        self.assertEqual(len(users), 0)
        options = {'minutes': 1, 'hours': 1}
        users = Request.objects.active_users(**options)
        self.assertEqual(len(users), 1)


class RequestQuerySetTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='foo')
        self.request = Request.objects.create(user=user, ip='1.2.3.4')

    def test_year(self):
        qs = Request.objects.all().year(self.request.time.year)
        self.assertEqual(qs.count(), 1)
        qs = Request.objects.all().year(self.request.time.year + 1)
        self.assertEqual(qs.count(), 0)

    def test_month(self):
        qs = Request.objects.all().month(year=None, month=None, date=now())
        self.assertEqual(qs.count(), 1)
        qs = Request.objects.all().month(year=None, month=None, date=date.today())
        self.assertEqual(qs.count(), 1)
        qs = Request.objects.all().month(
            year=None,
            month=None,
            date=now() - timedelta(days=31),
        )
        self.assertEqual(qs.count(), 0)

    def test_month_without_date(self):
        now_month = now().strftime('%b')
        qs = Request.objects.all().month(
            year=str(self.request.time.year),
            month=now_month
        )
        self.assertEqual(qs.count(), 1)
        previous_month = (now() - timedelta(days=31)).strftime('%b')
        qs = Request.objects.all().month(
            year=str(self.request.time.year),
            month=previous_month
        )
        self.assertEqual(qs.count(), 0)

    def test_month_without_date_year_and_month(self):
        self.assertRaises(TypeError, Request.objects.all().month)

    def test_month_without_date_invalid_year_or_month(self):
        qs = Request.objects.all().month(year='foo', month='Jan')
        self.assertIsNone(qs)
        qs = Request.objects.all().month(year='12', month='bar')
        self.assertIsNone(qs)

    def test_month_is_december(self):
        # setUp
        december_date = date(2015, 12, 1)
        self.request.time = december_date
        self.request.save()
        # Test
        qs = Request.objects.all().month(date=december_date)
        self.assertEqual(1, qs.count())

    def test_month_is_not_december(self):
        # setUp
        november_date = date(2015, 11, 1)
        self.request.time = november_date
        self.request.save()
        # Test
        qs = Request.objects.all().month(date=november_date)
        self.assertEqual(1, qs.count())

    def test_week(self):
        # setUp
        january_date = date(2015, 1, 6)
        self.request.time = january_date
        self.request.save()
        # Test
        qs = Request.objects.all().week(year='2015', week='1')
        self.assertEqual(qs.count(), 1)

    def test_week_invalid_year_or_week(self):
        qs = Request.objects.all().week(year='2015', week='foo')
        self.assertIsNone(qs)
        qs = Request.objects.all().week(year='foo', week='1')
        self.assertIsNone(qs)

    def test_day(self):
        qs = Request.objects.all().day(date=now())
        self.assertEqual(1, qs.count())
        qs = Request.objects.all().day(date=now() - timedelta(days=3))
        self.assertEqual(0, qs.count())

    def test_day_without_date(self):
        qs = Request.objects.all().day(
            year=str(now().year),
            month=now().strftime('%b'),
            day=str(now().day),
        )
        self.assertEqual(1, qs.count())

    def test_day_without_date_year_month_and_day(self):
        self.assertRaises(TypeError, Request.objects.all().day)

    def test_month_without_date_invalid_year_month_or_day(self):
        qs = Request.objects.all().day(year='foo', month='Jan', day='1')
        self.assertIsNone(qs)
        qs = Request.objects.all().day(year='12', month='bar', day='1')
        self.assertIsNone(qs)
        qs = Request.objects.all().day(year='12', month='Jan', day='foo')
        self.assertIsNone(qs)

    def test_today(self):
        # setUp
        request = Request.objects.create(ip='1.2.3.4')
        request.time = request.time - timedelta(days=3)
        request.save()
        # Test
        qs = Request.objects.all().today()
        self.assertEqual(1, qs.count())

    def test_this_year(self):
        # setUp
        request = Request.objects.create(ip='1.2.3.4')
        request.time = request.time - timedelta(days=700)
        request.save()
        # Test
        qs = Request.objects.all().this_year()
        self.assertEqual(1, qs.count())

    def test_this_month(self):
        # setUp
        request = Request.objects.create(ip='1.2.3.4')
        request.time = request.time - timedelta(days=60)
        request.save()
        # Test
        qs = Request.objects.all().this_month()
        self.assertEqual(1, qs.count())

    def test_this_week_today(self):
        qs = Request.objects.all().this_week()
        self.assertEqual(1, qs.count())

    def test_sunday_in_this_week_today(self):
        self.request.time -= timedelta(days=self.request.time.weekday())
        qs = Request.objects.all().this_week()
        self.assertEqual(1, qs.count())

    def test_this_week(self):
        # setUp
        request = Request.objects.create(ip='1.2.3.4')
        request.time = request.time - timedelta(days=21)
        request.save()
        # Test
        self.skipTest('Real error here before tests')
        qs = Request.objects.all().this_week()
        self.assertEqual(1, qs.count())

    def test_unique_visits(self):
        # setUp
        Request.objects.create(ip='1.2.3.4', referer=settings.BASE_URL)
        # Test
        qs = Request.objects.all().unique_visits()
        self.assertEqual(1, qs.count())

    def test_attr_list(self):
        attrs = Request.objects.all().attr_list('time')
        self.assertEqual(self.request.time, attrs[0])

    def test_search(self):
        Request.objects.all().search()
