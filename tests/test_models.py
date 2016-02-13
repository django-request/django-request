# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from request.models import Request


class RequestTests(unittest.TestCase):
    def test_from_http_request(self):
        http_request = HttpRequest()
        http_request.method = 'PATCH'
        http_request.path = '/kylef'
        http_request.META['REMOTE_ADDR'] = '32.64.128.16'
        http_request.META['HTTP_USER_AGENT'] = 'test user agent'
        http_request.META['HTTP_REFERER'] = 'https://fuller.li/'

        http_response = HttpResponse(status=204)

        request = Request()
        request.from_http_request(http_request, http_response, commit=False)

        self.assertEqual(request.path, '/kylef')
        self.assertEqual(request.method, 'PATCH')
        self.assertEqual(request.ip, '32.64.128.16')
        self.assertEqual(request.response, 204)
        self.assertEqual(request.user_agent, 'test user agent')
        self.assertEqual(request.referer, 'https://fuller.li/')

    def test_str_conversion(self):
        request = Request(method='PATCH', path='/', response=204)
        request.time = datetime.now()
        self.assertEqual(str(request), '[{}] PATCH / 204'.format(request.time))

    def test_browser_detection_with_no_ua(self):
        request = Request(method='GET', path='/', response=200)
        self.assertEqual(request.browser, None)

    def test_browser_detection_with_no_path(self):
        request = Request(
            user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0')
        self.assertEqual(request.browser, 'Firefox')

    def test_determining_search_keywords_with_no_referer(self):
        request = Request()
        self.assertEqual(request.keywords, None)

    def test_determining_search_keywords(self):
        request = Request(
            referer='https://www.google.com/search?client=safari&rls=en&q=querykit+core+data&ie=UTF-8&oe=UTF-8'
        )
        self.assertEqual(request.keywords, 'querykit core data')

    def test_request_data(self):
        data = {
            "login": "kylef",
            "id": 44164,
            "avatar_url": "https://avatars.githubusercontent.com/u/44164?v=3",
            "gravatar_id": "",
            "url": "https://api.github.com/users/kylef",
            "html_url": "https://github.com/kylef",
            "type": "User",
            "site_admin": False,
            "name": "Kyle Fuller",
            "company": "Apiary",
            "blog": "https://fuller.li/",
            "location": "London, England",
            "email": "kyle@fuller.li",
            "hireable": True,
            "bio": None,
            "public_repos": 152,
            "public_gists": 38,
            "followers": 806,
            "following": 89,
            "created_at": "2009-01-04T22:54:57Z",
            "updated_at": "2016-02-03T12:40:01Z"
        }
        request = Request(data=data)

        self.assertEqual(request.response, 200)
        self.assertDictEqual(request.data, data)
