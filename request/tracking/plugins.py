from datetime import timedelta
from django.utils.timezone import now
from request.plugins import set_count, Plugin
from request.tracking.models import Visitor
from request import settings


class ActiveVisitors(Plugin):
    def template_context(self):
        visitors = Visitor.objects.all().in_progress()
        since = now() - timedelta(**settings.VISIT_TIMEOUT)
        return {
            'since': since,
            'visitors': visitors,
        }
