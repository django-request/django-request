from django.conf import settings
from request.models import Request

class RequestMiddleware(object):
    def process_response(self, request, response):
        if request.is_ajax() and getattr(settings, 'REQUEST_IGNORE_AJAX', False):
            return response
        
        r = Request()
        r.from_http_request(request, response)
        
        return response
