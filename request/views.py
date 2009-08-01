from datetime import datetime, timedelta

from django.shortcuts import render_to_response
from django.db.models import Count
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

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
    
    # Example code for the graph, this could be changed to something far better.
    # This piece of code calculates amount of hits per day.
    days = 30 # Timespan from today to amount of days specified here.
    hits_coordinates = ""
    for x in range(days):
        hits_coordinates += "[%d,%d]," % (int((datetime.date(datetime.now()-timedelta(days=x))).strftime("%s"))*1000, Request.objects.filter(time__range=(datetime.date(datetime.now()-timedelta(days=x+1)),datetime.date(datetime.now()-timedelta(days=x)))).count())
    
    return render_to_response('admin/request/overview.html', {
        'title': _('Request overview'),
        'lastest_requests': Request.objects.all()[:5],
        'info_table': info_table,
        'hits_coordinates': hits_coordinates,
        'top_paths': Request.objects.paths(count=True, limit=10),
        
        'requests_url': '/admin/request/request/'
    }) 
