from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from request import settings


class VisitorQuerySet(models.query.QuerySet):
    def repeated(self):
        """Filter that has made at least two visits."""
        qs = self.annotate(visit_num=models.Count('visit'))
        return qs.filter(visit_num__gt=1)

    def new(self):
        """Filter that has not made any previous visits."""
        qs = self.annotate(visit_num=models.Count('visit'))
        return qs.filter(visit_num=1)

    def in_progress(self):
        """Filter that is currently visiting."""
        timeout = now() - timedelta(**settings.VISIT_TIMEOUT)
        return self.filter(requests__time__gte=timeout)


class VisitorManager(models.Manager):
    _queryset_class = VisitorQuerySet
    _queryset_proxy_methods = ['repeated', 'returned', 'new', 'in_progress']

    def __getattr__(self, attr, *args, **kwargs):
        if attr in self._queryset_proxy_methods:
            return getattr(self.get_query_set(), attr, None)
        super(VisitorManager, self).__getattr__(*args, **kwargs)


class VisitQuerySet(models.query.QuerySet):
    def in_progress(self):
        """Filter that in progress."""
        timeout = now() - timedelta(**settings.VISIT_TIMEOUT)
        return self.filter(requests__time__gte=timeout)

    def singleton(self):
        """Filter that in which only a single page is visited."""
        qs = self.annotate(request_num=models.Count('requests'))
        return qs.filter(request_num=1)


class VisitManager(models.Manager):
    _queryset_class = VisitQuerySet
    _queryset_proxy_methods = ['in_progress', 'singleton']

    def __getattr__(self, attr, *args, **kwargs):
        if attr in self._queryset_proxy_methods:
            return getattr(self.get_query_set(), attr, None)
        super(VisitManager, self).__getattr__(*args, **kwargs)
