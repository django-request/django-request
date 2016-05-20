from datetime import timedelta

from django.db import models
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from request.models import Request
from request.tracking.managers import VisitorManager, VisitManager
from request import settings


@python_2_unicode_compatible
class Visitor(models.Model):
    key = models.CharField(max_length=100)
    requests = models.ManyToManyField(Request)

    objects = VisitorManager()

    class Meta:
        app_label = 'tracking'
        verbose_name = _('visitor')
        verbose_name_plural = _('visitors')

    def __str__(self):
        return "#%s" % self.id

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:tracking_visitor_change', args=(self.id,))

    def hits(self):
        return self.requests.count()

    def visits(self):
        return self.visit_set.count()

    def first_time(self):
        try:
            return self.requests.order_by('time')[0].time
        except IndexError:
            return None

    def last_time(self):
        try:
            return self.requests.order_by('-time')[0].time
        except IndexError:
            return None

    def recency(self):
        """Time between two last visits."""
        raise NotImplementedError("Not yet!")

    def in_progress(self):
        """Return boolean representing active state of visitor"""
        return Visitor.objects.filter(id=self.id).in_progress().exists()


@python_2_unicode_compatible
class Visit(models.Model):
    visitor = models.ForeignKey(Visitor)
    requests = models.ManyToManyField(Request)

    objects = VisitManager()

    class Meta:
        app_label = 'tracking'
        verbose_name = _('visit')
        verbose_name_plural = _('visits')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('admin:tracking_visit_change', args=(self.id,))

    def hits(self):
        return self.requests.count()

    def first_time(self):
        try:
            return self.requests.order_by('time')[0].time
        except IndexError:
            return None

    def last_time(self):
        try:
            return self.requests.order_by('-time')[0].time
        except IndexError:
            return None

    def in_progress(self):
        """Return boolean representing active state of visit."""
        return Visit.objects.filter(id=self.id).in_progress().exists()


def add_requests_to_visitor(sender, instance, pk_set, **kwargs):
    timeout = now() - timedelta(**settings.VISIT_TIMEOUT)
    visits = Visit.objects.filter(visitor=instance,
                                  requests__time__gte=timeout)
    if visits.exists():
        visit = visits[0]
        visit.requests.add(*pk_set)
    else:
        visit = Visit.objects.create(visitor=instance)
        visit.requests.add(*pk_set)

m2m_changed.connect(add_requests_to_visitor, sender=Visitor.requests.through)
