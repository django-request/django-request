from django.test import TestCase

from request import router


class RegexPatternTest(TestCase):
    def test_init(self):
        router.RegexPattern(r'^foo$')

    def test_resolve(self):
        pat = router.RegexPattern(r'^foo$', 'bar')
        name, groups = pat.resolve('foo')
        self.assertEqual(name, 'bar')
        self.assertEqual(groups, {})

    def test_resolve_with_group(self):
        pat = router.RegexPattern(r'^foo(?P<id>\d*)$', 'bar')
        name, groups = pat.resolve('foo1')
        self.assertEqual(name, 'bar')
        self.assertIn('id', groups)
        self.assertEqual(groups['id'], '1')

    def test_cant_resolve(self):
        pat = router.RegexPattern(r'^foo$', 'bar')
        self.assertIsNone(pat.resolve('bar'))


class PatternsTest(TestCase):
    def setUp(self):
        self.unkn_pat = r'^foobar$'
        self.pat1 = r'^foo$'
        self.pat2 = r'^bar$'
        self.pats = router.Patterns(self.unkn_pat, self.pat1, self.pat2)

    def test_resolve(self):
        pat = self.pats.resolve('foo')
        self.assertEqual(pat, ('', {}))

    def test_cant_resolve(self):
        self.assertEqual(self.unkn_pat, self.pats.resolve('barfoo'))
