from django.test import TestCase
from request.tracking import plugins


class ActiveUsersTest(TestCase):
    def test_template_context(self):
        self.plugin = plugins.ActiveVisitors()
        context = self.plugin.template_context()
        self.assertEqual(0, context['visitors'].count())
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.template_context()
        self.assertEqual(1, context['visitors'].count())

    def test_render(self):
        self.plugin = plugins.ActiveVisitors()
        context = self.plugin.render()
        # 1st visit
        self.client.get('/admin/login')
        context = self.plugin.render()
