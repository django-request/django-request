import datetime
import time

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q
from django.utils import timezone

from .utils import BASE_URL, handle_naive_datetime

QUERYSET_PROXY_METHODS = (
    "year",
    "month",
    "week",
    "day",
    "today",
    "this_week",
    "this_month",
    "this_year",
    "unique_visits",
    "attr_list",
    "search",
)


class RequestQuerySet(models.query.QuerySet):
    def year(self, year):
        return self.filter(time__year=year)

    def month(self, year=None, month=None, month_format="%b", date=None):
        if not date:
            try:
                if year and month:
                    date = datetime.date(
                        *time.strptime(year + month, "%Y" + month_format)[:3]
                    )
                else:
                    raise TypeError("Request.objects.month() takes exactly 2 arguments")
            except ValueError:
                return
        # Truncate to date.
        if isinstance(date, datetime.datetime):
            date = date.date()
        # Calculate first and last day of month, for use in a date-range
        # lookup.
        first_day = datetime.datetime.combine(date.replace(day=1), datetime.time.min)
        last_day = first_day + relativedelta(months=1)
        return self.filter(
            time__gte=handle_naive_datetime(first_day),
            time__lt=handle_naive_datetime(last_day),
        )

    def week(self, year, week):
        try:
            date = datetime.date(*time.strptime(year + "-0-" + week, "%Y-%w-%U")[:3])
        except ValueError:
            return

        first_day = datetime.datetime.combine(date, datetime.time.min)
        last_day = first_day + datetime.timedelta(days=7)
        return self.filter(
            time__gte=handle_naive_datetime(first_day),
            time__lt=handle_naive_datetime(last_day),
        )

    def day(
        self,
        year=None,
        month=None,
        day=None,
        month_format="%b",
        day_format="%d",
        date=None,
    ):
        if not date:
            try:
                if year and month and day:
                    date = datetime.date(
                        *time.strptime(
                            year + month + day, "%Y" + month_format + day_format
                        )[:3]
                    )
                else:
                    raise TypeError("Request.objects.day() takes exactly 3 arguments")
            except ValueError:
                return
        return self.filter(
            time__range=(
                handle_naive_datetime(
                    datetime.datetime.combine(date, datetime.time.min)
                ),
                handle_naive_datetime(
                    datetime.datetime.combine(date, datetime.time.max)
                ),
            )
        )

    def today(self):
        return self.day(date=datetime.date.today())

    def this_year(self):
        return self.year(datetime.date.today().year)

    def this_month(self):
        return self.month(date=datetime.date.today())

    def this_week(self):
        today = datetime.date.today()
        return self.week(str(today.year), today.strftime("%U"))

    def unique_visits(self):
        return self.exclude(referer__startswith=BASE_URL)

    def attr_list(self, name):
        return [getattr(item, name, None) for item in self if hasattr(item, name)]

    def search(self):
        return self.filter(
            Q(referer__contains="google")
            | Q(referer__contains="yahoo")
            | Q(referer__contains="bing")
        )


class RequestManager(models.Manager):
    def __getattr__(self, attr, *args, **kwargs):
        if attr in QUERYSET_PROXY_METHODS:
            return getattr(self.get_queryset(), attr, None)
        super().__getattr__(*args, **kwargs)

    def get_queryset(self):
        return RequestQuerySet(self.model)

    def active_users(self, **options):
        """
        Returns a list of active users.

        Any arguments passed to this method will be
        given to timedelta for time filtering.

        Example:
        >>> Request.object.active_users(minutes=15)
        [<User: kylef>, <User: krisje8>]
        """

        qs = self.filter(user__isnull=False)

        if options:
            time = timezone.now() - datetime.timedelta(**options)
            qs = qs.filter(time__gte=time)

        requests = qs.select_related("user").only("user")

        return set([request.user for request in requests])
