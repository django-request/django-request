from django.utils.deprecation import MiddlewareMixin

from . import settings
from .models import Request
from .router import Patterns
from .utils import request_is_ajax


class RequestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.method.lower() not in settings.VALID_METHOD_NAMES:
            return response

        if response.status_code < 400 and settings.ONLY_ERRORS:
            return response

        ignore = Patterns(False, *settings.IGNORE_PATHS)
        if ignore.resolve(request.path[1:]):
            return response

        if request_is_ajax(request) and settings.IGNORE_AJAX:
            return response

        if request.META.get('REMOTE_ADDR') in settings.IGNORE_IP:
            return response

        ignore = Patterns(False, *settings.IGNORE_USER_AGENTS)
        if ignore.resolve(request.META.get('HTTP_USER_AGENT', '')):
            return response

        if getattr(request, 'user', False):
            if request.user.get_username() in settings.IGNORE_USERNAME:
                return response

        r = Request()
        r.from_http_request(request, response)

        return response
