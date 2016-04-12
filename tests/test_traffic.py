# -*- coding: utf-8 -*-
import mock
from django.test import TestCase
from django.core import exceptions
from request import traffic
from request.models import Request
from request import settings


class ModulesLoadTest(TestCase):
    def setUp(self):
        self.modules = traffic.Modules()

    def test_load(self):
        self.modules.load()
        for mod in self.modules._modules:
            self.assertIsInstance(mod, traffic.Module)

    @mock.patch('request.settings.REQUEST_TRAFFIC_MODULES',
                ('foobar',))
    def test_bad_module(self):
        self.assertRaises(exceptions.ImproperlyConfigured, self.modules.load)

    @mock.patch('request.settings.REQUEST_TRAFFIC_MODULES',
                ('foo.bar',))
    def test_import_error(self):
        self.assertRaises(exceptions.ImproperlyConfigured, self.modules.load)

    @mock.patch('request.settings.REQUEST_TRAFFIC_MODULES',
                ('request.traffic.Foo',))
    def test_module_not_exists(self):
        self.assertRaises(exceptions.ImproperlyConfigured, self.modules.load)


class ModulesModulesTest(TestCase):
    def setUp(self):
        self.modules = traffic.Modules()

    def test_loaded(self):
        self.modules.load()
        modules = self.modules.modules
        self.assertIsInstance(modules, list)

    def test_unloaded(self):
        modules = self.modules.modules
        self.assertIsInstance(modules, list)


class ModulesTableTest(TestCase):
    def setUp(self):
        self.modules = traffic.Modules()

    def test_table(self):
        queries = Request.objects.all()
        table = self.modules.table(queries)
        self.assertIsInstance(table, list)


class ModulesGraphTest(TestCase):
    def setUp(self):
        self.modules = traffic.Modules()

    def test_graph(self):
        queries = Request.objects.all()
        table = self.modules.graph(queries)
        self.assertIsInstance(table, list)


class ModuleBaseTest(TestCase):
    def test_init(self):
        module = traffic.Module()


class ModuleAjaxTest(TestCase):
    def test_count(self):
        module = traffic.Ajax()
        queries = Request.objects.all()
        module.count(queries)


class ModuleNotAjaxTest(TestCase):
    def test_count(self):
        module = traffic.NotAjax()
        queries = Request.objects.all()
        module.count(queries)


class ModuleErrorTest(TestCase):
    def test_count(self):
        module = traffic.Error()
        queries = Request.objects.all()
        module.count(queries)


class ModuleError404Test(TestCase):
    def test_count(self):
        module = traffic.Error404()
        queries = Request.objects.all()
        module.count(queries)


class ModuleHitTest(TestCase):
    def test_count(self):
        module = traffic.Hit()
        queries = Request.objects.all()
        module.count(queries)


class ModuleSearchTest(TestCase):
    def test_count(self):
        module = traffic.Search()
        queries = Request.objects.all()
        module.count(queries)


class ModuleSecureTest(TestCase):
    def test_count(self):
        module = traffic.Secure()
        queries = Request.objects.all()
        module.count(queries)


class ModuleUnsecureTest(TestCase):
    def test_count(self):
        module = traffic.Unsecure()
        queries = Request.objects.all()
        module.count(queries)


class ModuleUniqueVisitTest(TestCase):
    def test_count(self):
        module = traffic.UniqueVisit()
        queries = Request.objects.all()
        module.count(queries)


class ModuleUniqueVisitorTest(TestCase):
    def test_count(self):
        module = traffic.UniqueVisitor()
        queries = Request.objects.all()
        module.count(queries)


class ModuleUserTest(TestCase):
    def test_count(self):
        module = traffic.User()
        queries = Request.objects.all()
        module.count(queries)


class ModuleUniqueUserTest(TestCase):
    def test_count(self):
        module = traffic.UniqueUser()
        queries = Request.objects.all()
        module.count(queries)
