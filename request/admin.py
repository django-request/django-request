from datetime import datetime, timedelta, date

from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.utils.functional import update_wrapper
from django.template import RequestContext
from django.contrib import admin
from django.http import HttpResponse
from django.utils import simplejson

from request import settings
from request.models import Request
from request.traffic import modules

INFO_TABLE = ('today', 'this_week', 'this_month', 'this_year', 'all')
INFO_TABLE_QUERIES = [getattr(Request.objects, query, None)() for query in INFO_TABLE]

def set_count(items):
    """
    This is similar to "set", but this just creates a list with values.
    The list will be ordered from most frequent down.
    
    Example:
        >>> inventory = ['apple', 'lemon', 'apple', 'orange', 'lemon', 'lemon']
        >>> set_count(inventory)
        [('lemon', 3), ('apple', 2), ('orange', 1)]
    """
    item_count = {}
    for item in items:
        if not item: continue
        if not item_count.has_key(item): item_count[item] = 0
        item_count[item] += 1
    
    items = [(v, k) for k, v in item_count.iteritems()]
    items.sort()
    items.reverse()
    
    return [(k, v) for v, k in items]

class RequestAdmin(admin.ModelAdmin):
    list_display = ('time', 'path', 'response', 'method', 'request_from')
    fieldsets = (
        (_('Request'), {
            'fields': ('method', 'path', 'time', 'is_secure', 'is_ajax')
        }),
        (_('Response'), {
            'fields': ('response',)
        }),
        (_('User info'), {
            'fields': ('referer', 'user_agent', 'ip', 'user', 'language')
        })
    )
    
    def request_from(self, obj):
        if obj.user:
            return '<a href="?user__username=%s" title="%s">%s</a>' % (obj.user.username, _('Show only requests from this user.'), obj.user)
        return '<a href="?ip=%s" title="%s">%s</a>' % (obj.ip, _('Show only requests from this IP address.'), obj.ip)
    request_from.short_description = 'From'
    request_from.allow_tags = True
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        info = self.model._meta.app_label, self.model._meta.module_name
        
        return patterns('',
            url(r'^overview/$', wrap(self.overview), name='%s_%s_overview' % info),
            url(r'^overview/traffic.json$', wrap(self.traffic), name='%s_%s_traffic' % info),
        ) + super(RequestAdmin, self).get_urls()
    
    def overview(self, request):
        return render_to_response('admin/request/request/overview.html', {
            'title': _('Request overview'),
            
            'traffic_table': modules.table(INFO_TABLE_QUERIES),
            
            'lastest_requests': Request.objects.all()[:5],
            
            'top_paths': set_count(Request.objects.this_month().filter(response__lt=400).values_list('path', flat=True))[:10],
            'top_error_paths': set_count(Request.objects.this_month().filter(response__gte=400).values_list('path', flat=True))[:10],
            'top_referrers': set_count(Request.objects.this_month().unique_visits().values_list('referer', flat=True))[:10],
            'top_browsers': set_count(Request.objects.this_month().only('user_agent').attr_list('browser'))[:5],
            'top_search_phrases': set_count(Request.objects.this_month().search().only('referer').attr_list('keywords'))[:10],
            
            'use_hosted_media': settings.REQUEST_USE_HOSTED_MEDIA,
            'request_media_prefix': settings.REQUEST_MEDIA_PREFIX,
        }, context_instance=RequestContext(request))
    
    def traffic(self, request):
        try:
            days = int(request.GET.get('days', 30))
        except ValueError:
            days = 30
        
        days = [date.today() - timedelta(day) for day in range(days)]
        days_qs = [(day, Request.objects.day(date=day)) for day in days]
        return HttpResponse(simplejson.dumps(modules.graph(days_qs)), mimetype='text/javascript')

admin.site.register(Request, RequestAdmin)
