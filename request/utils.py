from django.utils.translation import ugettext_lazy as _

HTTP_STATUS_CODES = (
    # Infomational
    (100, _('Continue')),
    (101, _('Switching Protocols')),
    (102, _('Processing (WebDAV)')),
    
    # Success
    (200, _('OK')),
    (201, _('Created')),
    (202, _('Accepted')),
    (203, _('Non-Authoritative Information')),
    (204, _('No Content')),
    (205, _('Reset Content')),
    (206, _('Partial Content')),
    (207, _('Multi-Status (WebDAV)')),
    
    # Redirection
    (300, _('Multiple Choices')),
    (301, _('Moved Permanently')),
    (302, _('Found')),
    (303, _('See Other')),
    (304, _('Not Modified')),
    (305, _('Use Proxy')),
    (306, _('Switch Proxy')), # No longer used
    (307, _('Temporary Redirect')),
    
    # Client Error
    (400, _('Bad Request')),
    (401, _('Unauthorized')),
    (402, _('Payment Required')),
    (403, _('Forbidden')),
    (404, _('Not Found')),
    (405, _('Method Not Allowed')),
    (406, _('Not Acceptable')),
    (407, _('Proxy Authentication Required')),
    (408, _('Request Timeout')),
    (409, _('Conflict')),
    (410, _('Gone')),
    (411, _('Length Required')),
    (412, _('Precondition Failed')),
    (413, _('Request Entity Too Large')),
    (414, _('Request-URI Too Long')),
    (415, _('Unsupported Media Type')),
    (416, _('Requested Range Not Satisfiable')),
    (417, _('Expectation Failed')),
    (418, _('I\'m a teapot')), # April Fools
    (422, _('Unprocessable Entity (WebDAV)')),
    (423, _('Locked (WebDAV)')),
    (424, _('Failed Dependency (WebDAV)')),
    (425, _('Unordered Collection')),
    (426, _('Upgrade Required')),
    (449, _('Retry With')),
    
    # Server Error
    (500, _('Internal Server Error')),
    (501, _('Not Implemented')),
    (502, _('Bad Gateway')),
    (503, _('Service Unavailable')),
    (504, _('Gateway Timeout')),
    (505, _('HTTP Version Not Supported')),
    (506, _('Variant Also Negotiates')),
    (507, _('Insufficient Storage (WebDAV)')),
    (509, _('Bandwidth Limit Exceeded')),
    (510, _('Not Extended')),
)
