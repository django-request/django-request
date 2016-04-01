from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from request.models import Request


@python_2_unicode_compatible
class Visitor(models.Model):
    key = models.CharField(max_length=100)
    requests = models.ManyToManyField(Request)

    class Meta:
        verbose_name = _('visitor')
        verbose_name_plural = _('visitors')

    def __str__(self):
        return str(self.id)

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
