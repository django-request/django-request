from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from request.models import Request
from request.views import overview

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
            url(r'^overview/$', overview),
        )
        return my_urls + urls

admin.site.register(Request, RequestAdmin)
