from django.utils.translation import ugettext
from django.db.models import Count
from request import settings
from request.models import Request

unique_visitors = lambda days: {'data': [(int(day.strftime("%s"))*1000, Request.objects.day(date=day).aggregate(Count('ip', distinct=True))['ip__count']) for day in days], 'label':ugettext('Unique visitors')}
unique_visits = lambda days: {'data': [(int(day.strftime("%s"))*1000, Request.objects.day(date=day).exclude(referer__startswith=settings.REQUEST_BASE_URL).count()) for day in days], 'label':ugettext('Unique visits')}
hits = lambda days: {'data': [(int(day.strftime("%s"))*1000, Request.objects.day(date=day).count()) for day in days], 'label':ugettext('Hits')}
errors = lambda days: {'data': [(int(day.strftime("%s"))*1000, Request.objects.day(date=day).filter(response__gte=400).count()) for day in days], 'label':ugettext('Errors')}
