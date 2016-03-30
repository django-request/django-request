# -*- coding: utf-8 -*-
from django.test import TestCase
from request.templatetags.request_admin import trunc, pie_chart


class RequestAdminTruncTest(TestCase):
    def test_not_truncate(self):
        string = "A" * 10
        new_string = trunc(string, 20)
        self.assertEqual(len(new_string), 10)

    def test_truncate(self):
        string = "A" * 10
        new_string = trunc(string, 5)
        self.assertLess(len(new_string), 6)


class RequestAdminPieChart(TestCase):
    def test_pie_chart(self):
        inventory = ['apple', 'lemon', 'apple', 'orange', 'lemon', 'lemon']
        pie_chart(inventory)
