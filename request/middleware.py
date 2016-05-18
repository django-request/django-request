# -*- coding: utf-8 -*-
from request import settings
from request.models import Request
from request.router import patterns


class RequestMiddleware(object):
    def process_response(self, request, response):
        if request.method.lower() not in settings.REQUEST_VALID_METHOD_NAMES:
            return response

        if response.status_code < 400 and settings.REQUEST_ONLY_ERRORS:
            return response

        ignore = patterns(False, *settings.REQUEST_IGNORE_PATHS)
        if ignore.resolve(request.path[1:]):
            return response

        if request.is_ajax() and settings.REQUEST_IGNORE_AJAX:
            return response

        if request.META.get('REMOTE_ADDR') in settings.REQUEST_IGNORE_IP:
            return response

        ignore = patterns(False, *settings.REQUEST_IGNORE_USER_AGENTS)
        if ignore.resolve(request.META.get('HTTP_USER_AGENT', '')):
            return response

        if getattr(request, 'user', False):
            if request.user.username in settings.REQUEST_IGNORE_USERNAME:
                return response

        r = Request()
        r.from_http_request(request, response)

        return response
