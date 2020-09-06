from django.db.models import Count
from django.template.loader import render_to_string

from . import settings
from .models import Request
from .traffic import modules
from .utils import get_verbose_name


def set_count(items):
    '''
    This is similar to "set", but this just creates a list with values.
    The list will be ordered from most frequent down.

    Example:
        >>> inventory = ['apple', 'lemon', 'apple', 'orange', 'lemon', 'lemon']
        >>> set_count(inventory)
        [('lemon', 3), ('apple', 2), ('orange', 1)]
    '''
    item_count = {}
    for item in items:
        if not item:
            continue
        if item not in item_count:
            item_count[item] = 0
        item_count[item] += 1

    items = [(v, k) for k, v in item_count.items()]
    items.sort()
    items.reverse()

    return [(k, v) for v, k in items]


class Plugins:
    def load(self):
        from importlib import import_module

        from django.core import exceptions

        self._plugins = []
        for module_path in settings.PLUGINS:
            try:
                dot = module_path.rindex('.')
            except ValueError:
                raise exceptions.ImproperlyConfigured('{0} isn\'t a plugin'.format(module_path))
            plugin, plugin_classname = module_path[:dot], module_path[dot + 1:]

            try:
                mod = import_module(plugin)
            except ImportError as e:
                raise exceptions.ImproperlyConfigured('Error importing plugin {0}: "{1}"'.format(plugin, e))

            try:
                plugin_class = getattr(mod, plugin_classname)
            except AttributeError:
                raise exceptions.ImproperlyConfigured('Plugin "{0}" does not define a "{1}" class'.format(
                    plugin,
                    plugin_classname,
                ))

            self._plugins.append(plugin_class())

    def plugins(self):
        if not hasattr(self, '_plugins'):
            self.load()
        return self._plugins
    plugins = property(plugins)


plugins = Plugins()


class Plugin:
    def __init__(self):
        self.module_name = self.__class__.__name__

        if not hasattr(self, 'verbose_name'):
            self.verbose_name = get_verbose_name(self.module_name)

    def template_context(self):
        return {}

    def render(self):
        templates = [
            'request/plugins/{0}.html'.format(self.__class__.__name__.lower()),
            'request/plugins/base.html',
        ]

        if hasattr(self, 'template'):
            templates.insert(0, self.template)

        kwargs = self.template_context()
        kwargs['verbose_name'] = self.verbose_name
        kwargs['plugin'] = self
        return render_to_string(templates, kwargs)


class LatestRequests(Plugin):
    def template_context(self):
        return {'requests': Request.objects.all()[:5]}


class TrafficInformation(Plugin):
    def template_context(self):
        INFO_TABLE = ('today', 'this_week', 'this_month', 'this_year', 'all')
        INFO_TABLE_QUERIES = [getattr(Request.objects, query, None)() for query in INFO_TABLE]

        return {
            'traffic': modules.table(INFO_TABLE_QUERIES)
        }


class TopPaths(Plugin):
    def queryset(self):
        return self.qs.filter(response__lt=400)

    def template_context(self):
        return {
            'paths': self.queryset().values('path').annotate(Count('path')).order_by('-path__count')[:10]
        }


class TopErrorPaths(TopPaths):
    template = 'request/plugins/toppaths.html'

    def queryset(self):
        return self.qs.filter(response__gte=400)


class TopReferrers(Plugin):
    def queryset(self):
        return self.qs.unique_visits().exclude(referer='')

    def template_context(self):
        return {
            'referrers': self.queryset().values('referer').annotate(Count('referer')).order_by('-referer__count')[:10]
        }


class TopSearchPhrases(Plugin):
    def template_context(self):
        return {
            'phrases': set_count(self.qs.search().only('referer').attr_list('keywords'))[:10]
        }


class TopBrowsers(Plugin):
    def template_context(self):
        return {
            'browsers': set_count(self.qs.only('user_agent').attr_list('browser'))[:5]
        }


class ActiveUsers(Plugin):
    def template_context(self):
        return {}
