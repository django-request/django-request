from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

from request.models import Request
from request.views import overview, render_template

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
        urls = patterns('',
            url(r'^overview/$', overview),
            url(r'^jquery-1.3.2.min.js$', render_template('request/js/jquery-1.3.2.min.js'), name='request_jquery_js'),
            url(r'^jquery.flot.js$', render_template('request/js/jquery.flot.js'), name='request_jquery_flot_js'),
            url(r'^excanvas.min.js$', render_template('request/js/excanvas.min.js'), name='request_jquery_excanvas_flot_js'),
        )
        return urls + super(RequestAdmin, self).get_urls()

admin.site.register(Request, RequestAdmin)
