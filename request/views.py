from django.shortcuts import render_to_response
from django.db.models import Count
from request.models import Request
from datetime import datetime, timedelta


def overview(request):
    requests_all = Request.objects.all()
    requests_year = Request.objects.filter(time__gte=datetime(year=datetime.now().year, month=1, day=1))
    requests_month = Request.objects.filter(time__gte=datetime(year=datetime.now().year, month=datetime.now().month, day=1))
    requests_week = Request.objects.filter(time__gte=datetime.date(datetime.now() - timedelta(weeks=1)))
    requests_today = Request.objects.filter(time__gte=datetime.date(datetime.now()))
    
    lastrequests = requests_all[:5]
    hits = {
        'all': requests_all.count(),
        'year': requests_year.count(),
        'month': requests_month.count(),
        'week': requests_week.count(),
        'today': requests_today.count(),
    }
    visitors = {
        'all': requests_all.aggregate(Count('ip', distinct=True))['ip__count'],
        'year': requests_year.aggregate(Count('ip', distinct=True))['ip__count'],
        'month': requests_month.aggregate(Count('ip', distinct=True))['ip__count'],
        'week': requests_week.aggregate(Count('ip', distinct=True))['ip__count'],
        'today': requests_today.aggregate(Count('ip', distinct=True))['ip__count'],
    }
    
    return render_to_response('admin/request/overview.html', {'lastrequests': lastrequests, 'title': 'Request overview', 'hits': hits, 'visitors': visitors}) 
