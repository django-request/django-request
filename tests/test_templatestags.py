from django import template
from django.test import TestCase

from request.templatetags.request_tag import ActiveUserNode, active_users


# TODO: It's unused but add a parser: template.debug.DebugParser
class RequestTagActiveUserNodeTest(TestCase):
    def test_syntax_error_bad_args_number(self):
        token = template.base.Token(2, "active_users foo")
        self.assertRaises(template.TemplateSyntaxError, ActiveUserNode, None, token)

    def test_in_amount_duration_as_varname(self):
        token = template.base.Token(2, "active_users in 10 minutes as users")
        node = ActiveUserNode(None, token)
        self.assertEqual(node.as_varname, "users")

    def test_in_amount_duration_as_varname_error_bad_number(self):
        token = template.base.Token(2, "active_users in foo minutes as user_list")
        self.assertRaises(template.TemplateSyntaxError, ActiveUserNode, None, token)

    def test_as_varname(self):
        token = template.base.Token(2, "active_users as user_list")
        node = ActiveUserNode(None, token)
        self.assertEqual(node.as_varname, "user_list")

        token = template.base.Token(2, "active_users as users")
        node = ActiveUserNode(None, token)
        self.assertEqual(node.as_varname, "users")

    def test_no_args(self):
        token = template.base.Token(2, "active_users")
        ActiveUserNode(None, token)

    def test_render(self):
        token = template.base.Token(2, "active_users")
        node = ActiveUserNode(None, token)
        self.assertEqual("", node.render({}))


class RequestTagActiveUsersTest(TestCase):
    def test_active_users(self):
        token = template.base.Token(2, "active_users")
        node = active_users(None, token)
        self.assertIsInstance(node, ActiveUserNode)
