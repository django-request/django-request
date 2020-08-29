import mock
from django.core import exceptions
from django.test import TestCase

from request import plugins
from request.models import Request


class SetCountTestCase(TestCase):
    def test_set_count(self):
        inventory = ['apple', 'lemon', 'apple', 'orange', 'lemon', 'lemon']
        expected = [('lemon', 3), ('apple', 2), ('orange', 1)]
        result = plugins.set_count(inventory)
        self.assertEqual(result, expected)

    def test_set_count_false_items(self):
        inventory = ['apple', 'lemon', 'apple', 'orange', 'lemon', 'lemon',
                     None, False, '']
        expected = [('lemon', 3), ('apple', 2), ('orange', 1)]
        result = plugins.set_count(inventory)
        self.assertEqual(result, expected)


class PluginsLoadTest(TestCase):
    def setUp(self):
        self.plugins = plugins.Plugins()

    def test_load(self):
        self.plugins.load()
        for plu in self.plugins._plugins:
            self.assertIsInstance(plu, plugins.Plugin)

    @mock.patch('request.settings.PLUGINS',
                ('foobar',))
    def test_bad_module(self):
        self.assertRaises(exceptions.ImproperlyConfigured, self.plugins.load)

    @mock.patch('request.settings.PLUGINS',
                ('foo.bar',))
    def test_import_error(self):
        self.assertRaises(exceptions.ImproperlyConfigured, self.plugins.load)

    @mock.patch('request.settings.PLUGINS',
                ('request.plugins.Foo',))
    def test_module_not_exists(self):
        self.assertRaises(exceptions.ImproperlyConfigured, self.plugins.load)


class PluginsPluginsTest(TestCase):
    def setUp(self):
        self.plugins = plugins.Plugins()

    def test_loaded(self):
        self.plugins.load()
        plugins = self.plugins.plugins
        self.assertIsInstance(plugins, list)

    def test_unloaded(self):
        plugins = self.plugins.plugins
        self.assertIsInstance(plugins, list)


class PluginBaseTest(TestCase):
    def setUp(self):
        class TestPlugin(plugins.Plugin):
            '''
            Created for don't modify original class
            '''
        self.TestPlugin = TestPlugin

    def test_init(self):
        self.TestPlugin()
        # with verbose_name
        self.TestPlugin.verbose_name = 'foo'
        self.TestPlugin()

    def test_template_context(self):
        plugin = plugins.Plugin()
        self.assertEqual(plugin.template_context(), {})

    def test_render(self):
        plugin = plugins.Plugin()
        self.assertEqual(plugin.render(), '<h2>Plugin</h2>\n\n')
        # with template
        self.TestPlugin.template = 'bar'
        plugin = self.TestPlugin()
        self.assertEqual(plugin.render(), '<h2>Test Plugin</h2>\n\n')


class LatestRequestsTest(TestCase):
    def test_template_context(self):
        plugin = plugins.LatestRequests()
        context = plugin.template_context()
        self.assertIn('requests', context)


class TrafficInformationTest(TestCase):
    def test_template_context(self):
        plugin = plugins.TrafficInformation()
        context = plugin.template_context()
        self.assertIn('traffic', context)


class TopPathsTest(TestCase):
    def setUp(self):
        self.plugin = plugins.TopPaths()
        self.plugin.qs = Request.objects.all()

    def test_queryset(self):
        self.plugin.queryset()

    def test_template_context(self):
        context = self.plugin.template_context()
        self.assertIn('paths', context)


class TopErrorPathsTest(TestCase):
    def test_queryset(self):
        self.plugin = plugins.TopErrorPaths()
        self.plugin.qs = Request.objects.all()
        self.plugin.queryset()


class TopReferrersTest(TestCase):
    def setUp(self):
        self.plugin = plugins.TopReferrers()
        self.plugin.qs = Request.objects.all()

    def test_queryset(self):
        self.plugin.queryset()

    def test_template_context(self):
        context = self.plugin.template_context()
        self.assertIn('referrers', context)


class TopSearchPhrasesTest(TestCase):
    def test_template_context(self):
        self.plugin = plugins.TopSearchPhrases()
        self.plugin.qs = Request.objects.all()
        context = self.plugin.template_context()
        self.assertIn('phrases', context)


class TopBrowsersTest(TestCase):
    def test_template_context(self):
        self.plugin = plugins.TopBrowsers()
        self.plugin.qs = Request.objects.all()
        context = self.plugin.template_context()
        self.assertIn('browsers', context)


class ActiveUsersTest(TestCase):
    def test_template_context(self):
        self.plugin = plugins.ActiveUsers()
        self.plugin.template_context()
