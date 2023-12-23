import logging
import time
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils.deprecation import MiddlewareMixin

from . import settings
from .models import Request
from .router import Patterns
from .utils import request_is_ajax

logger = logging.getLogger('request.security.middleware')


class RequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()
        response = self.get_response(request)
        end_time = time.monotonic()
        response_time = timedelta(end_time - start_time)
        self.create_request_instance(request, response, response_time)
        return response

    def create_request_instance(self, request, response, response_time=None):
        """
        Method is repsonsible for creating a request.Request instance.  It also 
        provides a hook for capturing the generated instance for anyone that may want to 
        extend this middleware

        Args:
            request (django.http.HttpRequest): The django HttpRequest instance
            response (django.http.HttpResponse): The django HttpResponse instance
            response_time (float, optional): The request/response cycle time. Defaults to None.

        Returns:
            request.Request/None: The request.Request instance that was created or None
        """        
        if request.method.lower() not in settings.VALID_METHOD_NAMES:
            return 

        if response.status_code < 400 and settings.ONLY_ERRORS:
            return

        ignore = Patterns(False, *settings.IGNORE_PATHS)
        if ignore.resolve(request.path[1:]):
            return

        if request_is_ajax(request) and settings.IGNORE_AJAX:
            return 

        if request.META.get('REMOTE_ADDR') in settings.IGNORE_IP:
            return 

        ignore = Patterns(False, *settings.IGNORE_USER_AGENTS)
        if ignore.resolve(request.META.get('HTTP_USER_AGENT', '')):
            return 

        if getattr(request, 'user', False):
            if request.user.get_username() in settings.IGNORE_USERNAME:
                return 

        r = Request()
        try:
            r.from_http_request(request, response, response_time=response_time, commit=False)
            r.full_clean()
        except ValidationError as exc:
            logger.warning(
                'Bad request: %s',
                str(exc),
                exc_info=exc,
                extra={'status_code': 400, 'request': request},
            )
            return
        else:
            r.save()
            return r
        
