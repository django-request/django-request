# -*- coding: utf-8 -*-
from django.contrib.sessions.backends.db import SessionStore
from request.models import Request
from request.tracking.models import Visitor
from request import settings
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

        req = Request()
        req.from_http_request(request, response)

        if settings.USE_TRACKING:
            if 'track_key' in request.COOKIES:
                session_key = request.COOKIES['track_key']
            else:
                if hasattr(request, 'session'):
                    session_key = request.session._get_or_create_session_key()
                else:
                    session_key = SessionStore()._get_new_session_key()
                response.cookies['track_key'] = session_key
            visitor, created = Visitor.objects.get_or_create(key=session_key)
            visitor.requests.add(req)

        return response
