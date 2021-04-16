import json
from datetime import date, timedelta
from functools import update_wrapper

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Request
from .plugins import plugins
from .traffic import modules


class RequestAdmin(admin.ModelAdmin):
    list_display = ('time', 'path', 'response', 'method', 'request_from')
    fieldsets = (
        (_('Request'), {
            'fields': ('method', 'path', 'query_string', 'time', 'is_secure', 'is_ajax')
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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def request_from(self, obj):
        if obj.user_id:
            return format_html(
                '<a href="?user={0}" title="{1}">{2}</a>',
                obj.user_id,
                _('Show only requests from this user.'),
                obj.user,
            )
        return format_html(
            '<a href="?ip={0}" title="{1}">{0}</a>',
            obj.ip,
            _('Show only requests from this IP address.'),
        )
    request_from.short_description = 'From'
    request_from.allow_tags = True

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = (self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('overview/', wrap(self.overview), name='{0}_{1}_overview'.format(*info)),
            path('overview/traffic/', wrap(self.traffic), name='{0}_{1}_traffic'.format(*info)),
        ] + super().get_urls()

    def overview(self, request):
        qs = Request.objects.this_month()
        for plugin in plugins.plugins:
            plugin.qs = qs

        return render(
            request,
            'admin/request/request/overview.html',
            {
                'title': _('Request overview'),
                'plugins': plugins.plugins,
            }
        )

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

        days = [date.today() - timedelta(day) for day in range(0, days_count + 1, days_step)]
        days_qs = [(day, Request.objects.day(date=day)) for day in days]
        return HttpResponse(json.dumps(modules.graph(days_qs)), content_type='text/javascript')


admin.site.register(Request, RequestAdmin)
