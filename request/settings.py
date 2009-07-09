from django.conf import settings

REQUEST_IGNORE_AJAX = getattr(settings, 'REQUEST_IGNORE_AJAX', False)
