from django.conf import settings
from django.contrib.sites.models import Site

REQUEST_VALID_METHOD_NAMES = getattr(settings, 'REQUEST_VALID_METHOD_NAMES', ('get', 'post', 'put', 'delete', 'head', 'options', 'trace'))

REQUEST_ONLY_ERRORS = getattr(settings, 'REQUEST_ONLY_ERRORS', False)
REQUEST_IGNORE_AJAX = getattr(settings, 'REQUEST_IGNORE_AJAX', False)
REQUEST_IGNORE_IP = getattr(settings, 'REQUEST_IGNORE_IP', tuple())
REQUEST_LOG_IP = getattr(settings, 'REQUEST_LOG_IP', True)
REQUEST_IP_DUMMY = getattr(settings, 'REQUEST_IP_DUMMY', "1.1.1.1")
REQUEST_ANONYMOUS_IP = getattr(settings, 'REQUEST_ANONYMOUS_IP', False)
REQUEST_LOG_USER = getattr(settings, 'REQUEST_LOG_USER', True)
REQUEST_IGNORE_USERNAME = getattr(settings, 'REQUEST_IGNORE_USERNAME', tuple())
REQUEST_IGNORE_PATHS = getattr(settings, 'REQUEST_IGNORE_PATHS', tuple())

REQUEST_TRAFFIC_MODULES = getattr(settings, 'REQUEST_TRAFFIC_MODULES', (
    'request.traffic.UniqueVisitor',
    'request.traffic.UniqueVisit',
    'request.traffic.Hit',
))

REQUEST_PLUGINS = getattr(settings, 'REQUEST_PLUGINS', (
    'request.plugins.TrafficInformation',
    'request.plugins.LatestRequests',

    'request.plugins.TopPaths',
    'request.plugins.TopErrorPaths',
    'request.plugins.TopReferrers',
    'request.plugins.TopSearchPhrases',
    'request.plugins.TopBrowsers',
))

try:
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://%s' % Site.objects.get_current().domain)
except:
    REQUEST_BASE_URL = getattr(settings, 'REQUEST_BASE_URL', 'http://127.0.0.1')
