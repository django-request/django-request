from request.models import Request

class RequestMiddleware(object):
    def process_response(self, request, response):
        r = Request()
        r.from_http_request(request, response)
        
        return response
