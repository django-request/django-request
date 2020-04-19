# -*- coding: utf-8 -*-
from time import mktime

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Count
from django.utils.text import format_lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from . import settings
from .utils import get_verbose_name


class Modules(object):
    '''
    Set of :class:`.Module`.
    '''
    def load(self):
        '''
        Import and instanciate modules defined in
        ``settings.TRAFFIC_MODULES``.
        '''
        from importlib import import_module

        self._modules = ()
        for module_path in settings.TRAFFIC_MODULES:
            try:
                dot = module_path.rindex('.')
            except ValueError:
                raise ImproperlyConfigured('{0} isn\'t a traffic module'.format(module_path))
            traffic_module = module_path[:dot]
            traffic_classname = module_path[dot + 1:]

            try:
                mod = import_module(traffic_module)
            except ImportError as err:
                raise ImproperlyConfigured('Error importing module {0}: "{1}"'.format(traffic_module, err))

            try:
                traffic_class = getattr(mod, traffic_classname)
            except AttributeError:
                raise ImproperlyConfigured('Traffic module "{0}" does not define a "{1}" class'.format(
                    traffic_module,
                    traffic_classname,
                ))

            self._modules += (traffic_class(),)

    @property
    def modules(self):
        '''
        Get loaded modules, load them if isn't already made.
        '''
        if not hasattr(self, '_modules'):
            self.load()
        return self._modules

    def table(self, queries):
        '''
        Get a list of modules' counters.
        '''
        return tuple([(
            module.verbose_name_plural, [module.count(qs) for qs in queries]
        ) for module in self.modules])

    def graph(self, days):
        '''
        Get a list of modules' counters for all the given days.
        '''
        return tuple([{
            'data': [(mktime(day.timetuple()) * 1000, module.count(qs)) for day, qs in days],
            'label': str(gettext(module.verbose_name_plural)),
        } for module in self.modules])


modules = Modules()


class Module(object):
    '''
    Base module class.
    '''
    def __init__(self):
        self.module_name = self.__class__.__name__

        if not hasattr(self, 'verbose_name'):
            self.verbose_name = get_verbose_name(self.module_name)
        if not hasattr(self, 'verbose_name_plural'):
            self.verbose_name_plural = format_lazy('{}{}', self.verbose_name, 's')

    def count(self, qs):
        raise NotImplementedError('"count" isn\'t defined.')


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
        return qs.exclude(
            referer__startswith=settings.BASE_URL,
        ).count()


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
