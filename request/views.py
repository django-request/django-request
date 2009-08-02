from datetime import datetime, timedelta, date

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.db.models import Count
from django.contrib.sites.models import Site
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import simplejson
from django.http import HttpResponse

from request.models import Request

def overview(request):
    base_url = 'http://%s' % Site.objects.get_current().domain
    
    info_table = (
        (_('Unique visitors'), (
            Request.objects.today().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.this_week().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.this_month().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.this_year().aggregate(Count('ip', distinct=True))['ip__count'],
            Request.objects.aggregate(Count('ip', distinct=True))['ip__count']
        )), (_('Unique visits'), (
            Request.objects.today().exclude(referer__startswith=base_url).count(),
            Request.objects.this_week().exclude(referer__startswith=base_url).count(),
            Request.objects.this_month().exclude(referer__startswith=base_url).count(),
            Request.objects.this_year().exclude(referer__startswith=base_url).count(),
            Request.objects.exclude(referer__startswith=base_url).count(),
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
        
        'traffic_graph': simplejson.dumps([
            {'data': [(int(day.strftime("%s"))*1000, Request.objects.day(date=day).aggregate(Count('ip', distinct=True))['ip__count']) for day in days], 'label':ugettext('Unique visitors')},
            {'data': [(int(day.strftime("%s"))*1000, Request.objects.day(date=day).exclude(referer__startswith=base_url).count()) for day in days], 'label':ugettext('Unique visits')},
            {'data': [(int(day.strftime("%s"))*1000, Request.objects.day(date=day).count()) for day in days], 'label':ugettext('Hits')}
        ]),
        
        'top_paths': Request.objects.paths(count=True, limit=10, qs=Request.objects.exclude(response=404).exclude(response=500)),
        'top_error_paths': Request.objects.paths(count=True, limit=10, qs=(Request.objects.filter(response=404)|Request.objects.filter(response=500))),
        
        'requests_url': '/admin/request/request/'
    }) 

def render_template(template, content_type='text/javascript'):
    def wrap(request):
        jquery = render_to_string(template)
        return HttpResponse(jquery, content_type=content_type)
    return wrap
