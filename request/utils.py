# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .router import Patterns

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
    (306, _('Switch Proxy')),  # No longer used
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
    (418, _('I\'m a teapot')),  # April Fools
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


browsers = Patterns(
    ('Unknown', {}),
    # Browsers
    (r'AOL (?P<version>[\d+\.\d+]+)', 'AOL'),
    (
        r'Mozilla/(?P<mozilla_version>[-.\w]+) \(compatible; ( ?)MSIE (?P<msie_version>[-.\w]+); ' +
        r'( ?)( ?)America Online Browser (?P<version>[-.\w]+);',
        'AOL',
    ),
    (r'Camino/(?P<version>[-.\w]+)', 'Camino'),
    (r'Chrome/(?P<version>[-.\w]+)', 'Google Chrome'),
    (r'Firefox(/(?P<version>[-.\w]+)?)', 'Firefox'),
    (
        r'Mozilla/(?P<mozilla_version>[-.\w]+) \(compatible; ( ?)MSIE (?P<version>[-.\w]+); ' +
        r'( ?)( ?)(Win|Mac)',
        'Internet Explorer',
    ),
    (r'Konqueror/(?P<version>[-.\w]+)', 'Konqueror'),
    (r'Opera( |/)(?P<version>[-.\w]+)', 'Opera'),
    (r'OmniWeb(/(?P<version>[-.\w]+)?)', 'OmniWeb'),
    (r'Safari/(?P<version>[-.\w]+)', 'Safari'),
    (r'(Netscape([\d]?)|Navigator)/(?P<version>[-.\w]+)', 'Netscape'),
    (r'Wget/(?P<version>[-.\w]+)', 'Wget'),

    (r'Minefield(/(?P<version>[-.\w]+)?)', 'Firefox'),  # Firefox nightly trunk builds
    (r'Shiretoko(/(?P<version>[-.\w]+)?)', 'Firefox'),  # Firefox testing browser
    (r'GranParadiso(/(?P<version>[-.\w]+)?)', 'Firefox'),  # Firefox testing browser
    (r'Iceweasel(/(?P<version>[-.\w]+)?)', 'Firefox'),  # Debian re-branded firefox

    # RSS Reader
    (r'(NetNewsWire|NewsGatorOnline)/(?P<version>[-.\w]+)', 'NetNewsWire'),
    (r'Feedfetcher-Google', 'Google Reader'),

    # Bots
    (r'Googlebot', 'Google'),
    (r'Yahoo! Slurp', 'Yahoo'),
    (r'msnbot', 'MSN Bot'),
    (r'(Baiduspider|BaiduImagespider)', 'Baiduspider'),
    (r'Ask Jeeves', 'Ask Jeeves'),
    (r'FollowSite', 'FollowSite'),
    (r'WebAlta Crawler', 'WebAlta Crawler'),
    (r'ScoutJet', 'ScoutJet'),
    (r'SurveyBot', 'domaintools.com'),
    (r'Gigabot', 'Gigabot'),
    (r'Speedy Spider', 'entireweb'),
    (r'discobot', 'Discovery Engine'),
    (r'Purebot(/(?P<version>[-.\w]+)?);', 'Purity search'),
    (r'Yandex(/(?P<version>[-.\w]+)?)', 'Yandex'),
    (r'PostRank(/(?P<version>[-.\w]+)?)', 'PostRank'),
    (
        r'Mozilla/(?P<mozilla_version>[-.\w]+) \(compatible; DotBot/(?P<version>[-.\w]+); ' +
        r'http://www.dotnetdotcom.org/, crawler@dotnetdotcom.org\)',
        'Dotbot',
    ),
    (r'IrssiUrlLog(/(?P<version>[-.\w]+)?)', 'irssi'),
    (r'Linguee Bot \(http://www.linguee.com/bot; bot@linguee.com\)', 'Linguee'),
    (r'Sphider', 'Sphider'),

    # Other
    (r'Mediapartners-Google', 'Google Ads'),
    (r'Apple-PubSub', 'Apple-PubSub'),
    (r'Python-urllib', 'Python'),
)

engines = Patterns(
    None,
    (r'^https?:\/\/([\.\w]+)?yahoo.*(?:&|\?)p=(?P<keywords>[\+-_\w]+)', 'Yahoo'),
    (r'^https?:\/\/([\.\w]+)?google.*(?:&|\?)q=(?P<keywords>[\+-_\w]+)', 'Google'),
    (r'^https?:\/\/([\.\w]+)?bing.*(?:&|\?)q=(?P<keywords>[\+-_\w]+)', 'Bing'),
)


def get_verbose_name(class_name):
    '''
    Calculate the verbose_name by converting from InitialCaps to
    "lowercase with spaces".
    '''
    return re.sub(
        '(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))',
        ' \\1',
        class_name,
    ).strip()


def request_is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def handle_naive_datetime(value):
    if settings.USE_TZ and timezone.is_naive(value):
        return timezone.make_aware(value)
    return value
