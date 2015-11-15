from __future__ import unicode_literals
import unittest
from request.router import patterns

class PatternsTests(unittest.TestCase):
    def test_unnamed_patterns(self):
        self.assertEqual(patterns(False, r'^/admin/$').resolve('/admin/'),
                         ('', {}))
        self.assertEqual(patterns(False, r'^/admin/$').resolve('/login/'),
                         False)

    def test_named_patterns(self):
        named = patterns(False, (r'^/admin/$', 'name'))
        self.assertEqual(named.resolve('/admin/'),
                         ('name', {}))
        self.assertEqual(named.resolve('/login'),
                         False)

        named = patterns(False, [r'^/admin/$', 'name'])
        self.assertEqual(named.resolve('/admin/'),
                         ('name', {}))
        self.assertEqual(named.resolve('/login'),
                         False)
