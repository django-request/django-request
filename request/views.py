from datetime import datetime, timedelta, date

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson, importlib

from request.models import Request
from request import settings

def set_count(items):
    item_count = {}
    for item in items:
        if not item: continue
        if not item_count.has_key(item): item_count[item] = 0
        item_count[item] += 1
    
    items = [(v, k) for k, v in item_count.iteritems()]
    items.sort()
    items.reverse()
    
    return [(k, v) for v, k in items]

def overview(request):
    days = [date.today()-timedelta(day) for day in range(30)]
    browsers = set_count(Request.objects.attr_list('browser'))[:5]
    
    return render_to_response('admin/request/overview.html', {
        'title': _('Request overview'),
        'lastest_requests': Request.objects.all()[:5],
        'info_table': (
            (_('Unique visitors'), [getattr(Request.objects.all(), x, None)().aggregate(Count('ip', distinct=True))['ip__count'] for x in 'today', 'this_week', 'this_month', 'this_year', 'all']),
            (_('Unique visits'), [getattr(Request.objects.unique_visits(), x, None)().count() for x in 'today', 'this_week', 'this_month', 'this_year', 'all']),
            (_('Hits'), [getattr(Request.objects.all(), x, None)().count() for x in 'today', 'this_week', 'this_month', 'this_year', 'all'])
        ),
        'traffic_graph': simplejson.dumps([getattr(importlib.import_module(module_path[:module_path.rindex('.')]), module_path[module_path.rindex('.')+1:], None)(days) for module_path in settings.REQUEST_TRAFFIC_GRAPH_MODULES]),
        
        'top_paths': set_count(Request.objects.filter(response__lt=400).values_list('path', flat=True))[:10],
        'top_error_paths': set_count(Request.objects.filter(response__gte=400).values_list('path', flat=True))[:10],
        'top_referrers': set_count(Request.objects.unique_visits().values_list('referer', flat=True))[:10],
        'top_browsers': 'http://chart.apis.google.com/chart?cht=p3&chd=t:%s&chs=440x190&chl=%s' % (','.join([str(browser[1]) for browser in browsers]), '|'.join([browser[0] for browser in browsers])),
        
        'requests_url': '/admin/request/request/',
        'use_hosted_media': settings.REQUEST_USE_HOSTED_MEDIA
    }, context_instance=RequestContext(request)) 
