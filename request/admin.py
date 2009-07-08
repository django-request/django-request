from django.contrib import admin
from request.models import Request

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
        return obj.user or obj.ip
    request_from.short_description = 'From'

admin.site.register(Request, RequestAdmin)
