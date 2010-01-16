from django.conf import settings
from django.contrib.sites.models import Site

REQUEST_ONLY_ERRORS = getattr(settings, 'REQUEST_ONLY_ERRORS', False)
REQUEST_IGNORE_AJAX = getattr(settings, 'REQUEST_IGNORE_AJAX', False)
REQUEST_IGNORE_IP = getattr(settings, 'REQUEST_IGNORE_IP', tuple())
REQUEST_IGNORE_USERNAME = getattr(settings, 'REQUEST_IGNORE_USERNAME', tuple())

REQUEST_USE_HOSTED_MEDIA = getattr(settings, 'REQUEST_USE_HOSTED_MEDIA', True)

REQUEST_TRAFFIC_MODULES = getattr(settings, 'REQUEST_TRAFFIC_MODULES', (
    'request.traffic.UniqueVisitor',
    'request.traffic.UniqueVisit',
    'request.traffic.Hit',
))

try:
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://%s' % Site.objects.get_current().domain)
except:
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://127.0.0.1')
