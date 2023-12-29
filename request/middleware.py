import logging

from django.core.exceptions import ValidationError
from django.utils.deprecation import MiddlewareMixin
from django import get_version

from . import settings
from .models import Request
from .router import Patterns
from .utils import request_is_ajax

logger = logging.getLogger('request.security.middleware')


def _process_response(request, response):
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
    try:
        r.from_http_request(request, response, commit=False)
        r.full_clean()
    except ValidationError as exc:
        logger.warning(
            'Bad request: %s',
            str(exc),
            exc_info=exc,
            extra={'status_code': 400, 'request': request},
        )
    else:
        r.save()
    return response


class RequestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        return _process_response(request, response)


# Asynchronous support in django, introduced in this version
async_required_version = '3.1'

# Get the installed Django version
installed_version = get_version()

# Compare versions
installed_version_tuple = tuple(map(int, installed_version.split('.')))
required_version_tuple = tuple(map(int, async_required_version.split('.')))

# Provide async support for middleware, if the currently installed version of django supports it 
if installed_version_tuple >= required_version_tuple:
    import asyncio
    from django.utils.decorators import sync_and_async_middleware
    from asgiref.sync import sync_to_async

    @sync_and_async_middleware
    def RequestMiddleware(get_response):
        if asyncio.iscoroutinefunction(get_response):
            async def middleware(request):
                response = await get_response(request)
                response = await sync_to_async(_process_response, thread_sensitive=False)(request, response)
                return response

        else:
            def middleware(request):
                response = get_response(request)
                response = _process_response(request, response)
                return response

        return middleware
