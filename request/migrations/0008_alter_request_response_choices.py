from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0007_alter_request_is_ajax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='response',
            field=models.SmallIntegerField(choices=[(100, 'Continue'), (101, 'Switching Protocols'), (102, 'Processing (WebDAV)'), (103, 'Early Hints'), (200, 'OK'), (201, 'Created'), (202, 'Accepted'), (203, 'Non-Authoritative Information'), (204, 'No Content'), (205, 'Reset Content'), (206, 'Partial Content'), (207, 'Multi-Status (WebDAV)'), (208, 'Already Reported (WebDAV)'), (226, 'IM Used (HTTP Delta encoding)'), (300, 'Multiple Choices'), (301, 'Moved Permanently'), (302, 'Found'), (303, 'See Other'), (304, 'Not Modified'), (305, 'Use Proxy'), (306, 'Switch Proxy'), (307, 'Temporary Redirect'), (308, 'Permanent Redirect'), (400, 'Bad Request'), (401, 'Unauthorized'), (402, 'Payment Required'), (403, 'Forbidden'), (404, 'Not Found'), (405, 'Method Not Allowed'), (406, 'Not Acceptable'), (407, 'Proxy Authentication Required'), (408, 'Request Timeout'), (409, 'Conflict'), (410, 'Gone'), (411, 'Length Required'), (412, 'Precondition Failed'), (413, 'Request Entity Too Large'), (414, 'Request-URI Too Long'), (415, 'Unsupported Media Type'), (416, 'Requested Range Not Satisfiable'), (417, 'Expectation Failed'), (418, "I'm a teapot"), (422, 'Unprocessable Entity (WebDAV)'), (423, 'Locked (WebDAV)'), (424, 'Failed Dependency (WebDAV)'), (425, 'Unordered Collection'), (426, 'Upgrade Required'), (428, 'Precondition Required'), (429, 'Too Many Requests'), (431, 'Request Header Fields Too Large'), (449, 'Retry With'), (451, 'Unavailable For Legal Reasons'), (500, 'Internal Server Error'), (501, 'Not Implemented'), (502, 'Bad Gateway'), (503, 'Service Unavailable'), (504, 'Gateway Timeout'), (505, 'HTTP Version Not Supported'), (506, 'Variant Also Negotiates'), (507, 'Insufficient Storage (WebDAV)'), (509, 'Bandwidth Limit Exceeded'), (510, 'Not Extended'), (511, 'Network Authentication Required')], default=200, verbose_name='response'),
        ),
    ]
