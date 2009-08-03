from datetime import datetime, timedelta, date

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson, importlib

from request.models import Request
from request import settings

def overview(request):
    info_table = (
        (_('Unique visitors'), (
            Request.objects.today().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.this_week().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.this_month().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.this_year().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.aggregate(Count('ip', distinct=True))['ip__count']
        )), (_('Unique visits'), (
            Request.objects.today().exclude(referer__startswith=settings.REQUEST_BASE_URL).count(),
            Request.objects.this_week().exclude(referer__startswith=settings.REQUEST_BASE_URL).count(),
            Request.objects.this_month().exclude(referer__startswith=settings.REQUEST_BASE_URL).count(),
            Request.objects.this_year().exclude(referer__startswith=settings.REQUEST_BASE_URL).count(),
            Request.objects.exclude(referer__startswith=settings.REQUEST_BASE_URL).count(),
        )), (_('Hits'), (
            Request.objects.today().count(),
            Request.objects.this_week().count(),
            Request.objects.this_month().count(),
            Request.objects.this_year().count(),
            Request.objects.count(),
        ))
    )
    
    days = [date.today()-timedelta(day) for day in range(30)]
    
    return render_to_response('admin/request/overview.html', {
        'title': _('Request overview'),
        'lastest_requests': Request.objects.all()[:5],
        'info_table': info_table,
        'traffic_graph': simplejson.dumps([getattr(importlib.import_module(module_path[:module_path.rindex('.')]), module_path[module_path.rindex('.')+1:], None)(days) for module_path in settings.REQUEST_TRAFFIC_GRAPH_MODULES]),
        'top_paths': Request.objects.paths(count=True, limit=10, qs=Request.objects.filter(response__lt=400)),
        'top_error_paths': Request.objects.paths(count=True, limit=10, qs=(Request.objects.filter(response__gte=400))),
        'top_referrers': Request.objects.referrers(count=True, limit=10, qs=Request.objects.exclude(referer__startswith=settings.REQUEST_BASE_URL).exclude(referer='')),
        
        'requests_url': '/admin/request/request/',
        'use_hosted_media': settings.REQUEST_USE_HOSTED_MEDIA
    }, context_instance=RequestContext(request)) 
