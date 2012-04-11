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
from request.plugins import *


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
    raw_id_fields = ('user',)
    readonly_fields = ('time',)

    def lookup_allowed(self, key, value):
        return key == 'user__username' or super(RequestAdmin, self).lookup_allowed(key, value)

    def request_from(self, obj):
        if obj.user_id:
            user = obj.get_user()
            return '<a href="?user__username=%s" title="%s">%s</a>' % (user.username, _('Show only requests from this user.'), user)
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
        qs = Request.objects.this_month()
        for plugin in plugins.plugins:
            plugin.qs = qs

        return render_to_response('admin/request/request/overview.html', {
            'title': _('Request overview'),
            'plugins': plugins.plugins,
        }, context_instance=RequestContext(request))

    def traffic(self, request):
        try:
            days_count = int(request.GET.get('days', 30))
        except ValueError:
            days_count = 30

        if days_count < 10:
            days_step = 1
        elif days_count < 60:
            days_step = 2
        else:
            days_step = 30

        days = [date.today() - timedelta(day) for day in xrange(0, days_count, days_step)]
        days_qs = [(day, Request.objects.day(date=day)) for day in days]
        return HttpResponse(simplejson.dumps(modules.graph(days_qs)), mimetype='text/javascript')

admin.site.register(Request, RequestAdmin)
