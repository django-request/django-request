# -*- coding: utf-8 -*-
import re
from time import mktime

from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat, ugettext
from request import settings

# Calculate the verbose_name by converting from InitialCaps to "lowercase with spaces".
get_verbose_name = lambda class_name: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', ' \\1', class_name).strip()


class Modules(object):
    def load(self):
        from importlib import import_module
        from django.core import exceptions

        self._modules = []
        for module_path in settings.REQUEST_TRAFFIC_MODULES:
            try:
                dot = module_path.rindex('.')
            except ValueError:
                raise exceptions.ImproperlyConfigured('%s isn\'t a traffic module' % module_path)
            traffic_module, traffic_classname = module_path[:dot], module_path[dot + 1:]

            try:
                mod = import_module(traffic_module)
            except ImportError as e:
                raise exceptions.ImproperlyConfigured('Error importing module %s: "%s"' % (traffic_module, e))

            try:
                traffic_class = getattr(mod, traffic_classname)
            except AttributeError:
                raise exceptions.ImproperlyConfigured('Traffic module "%s" does not define a "%s" class' % (traffic_module, traffic_classname))

            self._modules.append(traffic_class())

    def modules(self):
        if not hasattr(self, '_modules'):
            self.load()
        return self._modules
    modules = property(modules)

    def table(self, queries):
        return [(module.verbose_name_plural, [module.count(qs) for qs in queries]) for module in self.modules]

    def graph(self, days):
        return [{'data': [(mktime(day.timetuple()) * 1000, module.count(qs)) for day, qs in days], 'label':ugettext(module.verbose_name_plural)} for module in self.modules]

modules = Modules()


class Module(object):
    def __init__(self):
        self.module_name = self.__class__.__name__

        if not hasattr(self, 'verbose_name'):
            self.verbose_name = _(get_verbose_name(self.module_name))
        if not hasattr(self, 'verbose_name_plural'):
            self.verbose_name_plural = string_concat(self.verbose_name, 's')


class Ajax(Module):
    verbose_name_plural = _('Ajax')

    def count(self, qs):
        return qs.filter(is_ajax=True).count()


class NotAjax(Module):
    verbose_name = _('Not Ajax')
    verbose_name_plural = _('Not Ajax')

    def count(self, qs):
        return qs.filter(is_ajax=False).count()


class Error(Module):
    verbose_name = _('Error')
    verbose_name_plural = _('Errors')

    def count(self, qs):
        return qs.filter(response__gte=400).count()


class Error404(Module):
    verbose_name = _('Error 404')
    verbose_name_plural = _('Errors 404')

    def count(self, qs):
        return qs.filter(response=404).count()


class Hit(Module):
    verbose_name = _('Hit')
    verbose_name_plural = _('Hits')

    def count(self, qs):
        return qs.count()


class Search(Module):
    verbose_name = _('Search')
    verbose_name_plural = _('Searches')

    def count(self, qs):
        return qs.search().count()


class Secure(Module):
    verbose_name = _('Secure')
    verbose_name_plural = _('Secure')

    def count(self, qs):
        return qs.filter(is_secure=True).count()


class Unsecure(Module):
    verbose_name = _('Unsecure')
    verbose_name_plural = _('Unsecure')

    def count(self, qs):
        return qs.filter(is_secure=False).count()


class UniqueVisit(Module):
    verbose_name = _('Unique Visit')
    verbose_name_plural = _('Unique Visits')

    def count(self, qs):
        return qs.exclude(referer__startswith=settings.REQUEST_BASE_URL).count()


class UniqueVisitor(Module):
    verbose_name = _('Unique Visitor')
    verbose_name_plural = _('Unique Visitor')

    def count(self, qs):
        return qs.aggregate(Count('ip', distinct=True))['ip__count']


class User(Module):
    verbose_name = _('User')
    verbose_name_plural = _('User')

    def count(self, qs):
        return qs.exclude(user__isnull=False).count()


class UniqueUser(Module):
    verbose_name = _('Unique User')
    verbose_name_plural = _('Unique User')

    def count(self, qs):
        return qs.aggregate(Count('user', distinct=True))['user__count']
