# -*- coding: utf-8 -*-
from request import settings
from request.models import Request
from request.router import patterns


try:
    # needed to support Django >= 1.10 MIDDLEWARE
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # needed to keep Django <= 1.9 MIDDLEWARE_CLASSES
    MiddlewareMixin = object


class RequestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.method.lower() not in settings.VALID_METHOD_NAMES:
            return response

        if response.status_code < 400 and settings.ONLY_ERRORS:
            return response

        ignore = patterns(False, *settings.IGNORE_PATHS)
        if ignore.resolve(request.path[1:]):
            return response

        if request.is_ajax() and settings.IGNORE_AJAX:
            return response

        if request.META.get('REMOTE_ADDR') in settings.IGNORE_IP:
            return response

        ignore = patterns(False, *settings.IGNORE_USER_AGENTS)
        if ignore.resolve(request.META.get('HTTP_USER_AGENT', '')):
            return response

        if getattr(request, 'user', False):
            if request.user.username in settings.IGNORE_USERNAME:
                return response

        r = Request()
        r.from_http_request(request, response)

        return response
