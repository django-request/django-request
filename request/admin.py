from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.shortcuts import render_to_response
from request.models import Request
from datetime import datetime, timedelta

class RequestAdmin(admin.ModelAdmin):
    list_display = ('time', 'path', 'response', 'method', 'request_from')
    fieldsets = (
        ('Request', {
            'fields': ('method', 'path', 'time', 'is_secure', 'is_ajax')
        }),
        ('Response', {
            'fields': ('response',)
        }),
        ('User info', {
            'fields': ('referer', 'user_agent', 'ip', 'user', 'language')
        })
    )
    
    def request_from(self, obj):
        if obj.user:
            return '<a href="?user__username=%s" title="Show only requests from this user.">%s</a>' % (obj.user.username, obj.user)
        return '<a href="?ip=%s" title="Show only requests from this IP address.">%s</a>' % (obj.ip, obj.ip)
    request_from.short_description = 'From'
    request_from.allow_tags = True
    
    def get_urls(self):
        urls = super(RequestAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^overview/$', self.overview),
        )
        return my_urls + urls
    
    def overview(self, request):
        requests_all = Request.objects.all()
        requests_year = Request.objects.filter(time__gte=datetime(year=datetime.now().year, month=1, day=1))
        requests_month = Request.objects.filter(time__gte=datetime(year=datetime.now().year, month=datetime.now().month, day=1))
        requests_week = Request.objects.filter(time__gte=datetime.date(datetime.now() - timedelta(weeks=1)))
        requests_today = Request.objects.filter(time__gte=datetime.date(datetime.now()))
        
        lastrequests = requests_all[:5]
        hits = {'all': requests_all.count(),'year': requests_year.count(), 'month': requests_month.count(), 'week': requests_week.count(), 'today': requests_today.count()}
        
        return render_to_response('admin/request/overview.html', {'lastrequests': lastrequests, 'title': 'Request overview', 'hits': hits})

admin.site.register(Request, RequestAdmin)
