from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from request.tracking.models import Visitor


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('key', 'hits', 'first_time', 'last_time')
    fieldsets = ()

    def lookup_allowed(self, key, value):
        return key == 'requests__user__username' or super(VisitorAdmin, self).lookup_allowed(key, value)

    def hits(self, obj):
        return obj.requests.count()

    def request_from(self, obj):
        if obj.user_id:
            user = obj.get_user()
            return '<a href="?user__username=%s" title="%s">%s</a>' % (user.username, _('Show only requests from this user.'), user)
        return '<a href="?ip=%s" title="%s">%s</a>' % (obj.ip, _('Show only requests from this IP address.'), obj.ip)
    request_from.short_description = 'From'
    request_from.allow_tags = True

admin.site.register(Visitor, VisitorAdmin)
