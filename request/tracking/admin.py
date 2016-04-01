from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from request.tracking.models import Visitor, Visit


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('key', 'hits', 'visits', 'first_time', 'last_time')
    fieldsets = ()

    def lookup_allowed(self, key, value):
        return key == 'requests__user__username' or super(VisitorAdmin, self).lookup_allowed(key, value)

    def hits(self, obj):
        return obj.requests.count()

    def visits(self, obj):
        return obj.visit_set.count()


class VisitAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'hits', 'first_time', 'last_time')
    fieldsets = ()

    def lookup_allowed(self, key, value):
        return key == 'requests__user__username' or super(VisitorAdmin, self).lookup_allowed(key, value)

    def hits(self, obj):
        return obj.requests.count()


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Visit, VisitAdmin)
