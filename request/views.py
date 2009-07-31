from django.shortcuts import render_to_response
from django.db.models import Count
from django.contrib.sites.models import Site
from request.models import Request
from datetime import datetime, timedelta


def overview(request):
    requests_all = Request.objects.all()
    requests_year = Request.objects.filter(time__gte=datetime(year=datetime.now().year, month=1, day=1))
    requests_month = Request.objects.filter(time__gte=datetime(year=datetime.now().year, month=datetime.now().month, day=1))
    requests_week = Request.objects.filter(time__gte=datetime.date(datetime.now() - timedelta(weeks=1)))
    requests_today = Request.objects.filter(time__gte=datetime.date(datetime.now()))
    
    base_url = 'http://%s' % Site.objects.get_current().domain
    
    lastrequests = requests_all[:5]
    hits = {
        'all': requests_all.count(),
        'year': requests_year.count(),
        'month': requests_month.count(),
        'week': requests_week.count(),
        'today': requests_today.count(),
    }
    visits = {
        'all': requests_all.exclude(referer__startswith=base_url).count(),
        'year': requests_year.exclude(referer__startswith=base_url).count(),
        'month': requests_month.exclude(referer__startswith=base_url).count(),
        'week': requests_week.exclude(referer__startswith=base_url).count(),
        'today': requests_today.exclude(referer__startswith=base_url).count(),
    }
    visitors = {
        'all': requests_all.aggregate(Count('ip', distinct=True))['ip__count'],
        'year': requests_year.aggregate(Count('ip', distinct=True))['ip__count'],
        'month': requests_month.aggregate(Count('ip', distinct=True))['ip__count'],
        'week': requests_week.aggregate(Count('ip', distinct=True))['ip__count'],
        'today': requests_today.aggregate(Count('ip', distinct=True))['ip__count'],
    }
    
    # Example code for the graph, this could be changed to something far better.
    # This piece of code calculates amount of hits per day.
    days = 30 # Timespan from today to amount of days specified here.
    hits_coordinates = ""
    for x in range(days):
        hits_coordinates += "[%d,%d]," % (int((datetime.date(datetime.now()-timedelta(days=x))).strftime("%s"))*1000, Request.objects.filter(time__range=(datetime.date(datetime.now()-timedelta(days=x+1)),datetime.date(datetime.now()-timedelta(days=x)))).count())
    
    return render_to_response('admin/request/overview.html', {'lastrequests': lastrequests, 'title': 'Request overview', 'hits': hits, 'visits': visits, 'visitors': visitors, 'hits_coordinates': hits_coordinates}) 
