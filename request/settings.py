from django.conf import settings
from django.contrib.sites.models import Site

REQUEST_IGNORE_AJAX = getattr(settings, 'REQUEST_IGNORE_AJAX', False)
REQUEST_IGNORE_IP = getattr(settings, 'REQUEST_IGNORE_IP', tuple())
REQUEST_IGNORE_USERNAME = getattr(settings, 'REQUEST_IGNORE_USERNAME', tuple())

REQUEST_USE_HOSTED_MEDIA = getattr(settings, 'REQUEST_USE_HOSTED_MEDIA', True)

REQUEST_TRAFFIC_GRAPH_MODULES = getattr(settings, 'REQUEST_TRAFFIC_GRAPH_MODULES', (
    'request.traffic_module.unique_visitors',
    'request.traffic_module.unique_visits',
    'request.traffic_module.hits',
))

REQUEST_BASE_URL = 'http://%s' % Site.objects.get_current().domain
