import datetime

from django.test import SimpleTestCase
from django.test.utils import override_settings
from django.utils import timezone

from request.utils import handle_naive_datetime

EAT = timezone.get_fixed_timezone(180)  # Africa/Nairobi
ICT = timezone.get_fixed_timezone(420)  # Asia/Bangkok


class UtilsTests(SimpleTestCase):
    @override_settings(USE_TZ=False)
    def test_handle_naive_datetime_no_tz(self):
        naive_datetime = datetime.datetime(2017, 10, 15, 0, 0, 0, 0)
        self.assertEqual(handle_naive_datetime(naive_datetime), naive_datetime)

    @override_settings(USE_TZ=True, TIME_ZONE='Africa/Nairobi')
    def test_handle_naive_datetime_tz_aware(self):
        aware_datetime = datetime.datetime(2017, 10, 15, 0, 0, 0, 0, tzinfo=ICT)
        self.assertEqual(handle_naive_datetime(aware_datetime), aware_datetime)

    @override_settings(USE_TZ=True, TIME_ZONE='Africa/Nairobi')
    def test_handle_naive_datetime_tz_naive(self):
        naive_datetime = datetime.datetime(2017, 10, 15, 0, 0, 0, 0)
        self.assertEqual(
            handle_naive_datetime(naive_datetime),
            datetime.datetime(2017, 10, 15, 0, 0, 0, 0, tzinfo=EAT),
        )
