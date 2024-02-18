import datetime

from django.conf import settings
from django.test import SimpleTestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.functional import SimpleLazyObject

from request import utils
from request.utils import handle_naive_datetime

EAT = timezone.get_fixed_timezone(180)  # Africa/Nairobi
ICT = timezone.get_fixed_timezone(420)  # Asia/Bangkok


class UtilsTests(SimpleTestCase):
    @override_settings(USE_TZ=False)
    def test_handle_naive_datetime_no_tz(self):
        naive_datetime = datetime.datetime(2017, 10, 15, 0, 0, 0, 0)
        self.assertEqual(handle_naive_datetime(naive_datetime), naive_datetime)

    @override_settings(USE_TZ=True, TIME_ZONE="Africa/Nairobi")
    def test_handle_naive_datetime_tz_aware(self):
        aware_datetime = datetime.datetime(2017, 10, 15, 0, 0, 0, 0, tzinfo=ICT)
        self.assertEqual(handle_naive_datetime(aware_datetime), aware_datetime)

    @override_settings(USE_TZ=True, TIME_ZONE="Africa/Nairobi")
    def test_handle_naive_datetime_tz_naive(self):
        naive_datetime = datetime.datetime(2017, 10, 15, 0, 0, 0, 0)
        self.assertEqual(
            handle_naive_datetime(naive_datetime),
            datetime.datetime(2017, 10, 15, 0, 0, 0, 0, tzinfo=EAT),
        )

    def test_base_url(self):
        utils.BASE_URL = SimpleLazyObject(utils.get_base_url)
        self.assertEqual(utils.BASE_URL, "http://127.0.0.1")

    def test_base_url_request_base_url(self):
        settings.REQUEST_BASE_URL = "http://othersite.com"
        utils.BASE_URL = SimpleLazyObject(utils.get_base_url)
        self.assertEqual(utils.BASE_URL, "http://othersite.com")
