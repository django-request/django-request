from django.conf import settings

REQUEST_IGNORE_AJAX = getattr(settings, 'REQUEST_IGNORE_AJAX', False)
REQUEST_IGNORE_IP = getattr(settings, 'REQUEST_IGNORE_IP', tuple())
REQUEST_IGNORE_USERNAME = getattr(settings, 'REQUEST_IGNORE_USERNAME', tuple())

REQUEST_USE_HOSTED_MEDIA = getattr(settings, 'REQUEST_USE_HOSTED_MEDIA', True)
