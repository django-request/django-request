# -*- coding: utf-8 -*-
from django import template
from request.models import Request

register = template.Library()


class ActiveUserNode(template.Node):
    def __init__(self, parser, token):
        tokens = token.contents.split()
        tag_name = tokens.pop(0)
        self.kwargs = {}

        if not ((len(tokens) == 5) or (len(tokens) == 2) or (len(tokens) == 0)):
            raise template.TemplateSyntaxError("Incorrect amount of arguments in the tag %r" % tag_name)

        if (len(tokens) == 5) and (tokens[0] == 'in'):
            tokens.pop(0)  # pop 'in' of tokens
            try:
                self.kwargs[str(tokens.pop(0))] = int(tokens.pop(0))
            except ValueError:
                raise template.TemplateSyntaxError('Invalid arguments for %r template tag.' % tag_name)
        else:
            self.kwargs['minutes'] = 15

        if (len(tokens) == 2 and (tokens[0] == 'as')):
            self.as_varname = tokens[1]
        else:
            self.as_varname = 'user_list'

    def render(self, context):
        context[self.as_varname] = Request.objects.active_users(**self.kwargs)
        return ''


@register.tag
def active_users(parser, token):
    """
    This template tag will get a list of active users based on time,
    if you do not supply a time to the tag, the default of 15 minutes
    will be used. With the 'as' clause you can supply what context
    variable you want the user list to be. There is also a 'in' clause,
    after in you would specify a amount and a duration. Such as 2 hours,
    of 10 minutes.

    Syntax::
        {% active_users in [amount] [duration] as [varname] %}
        {% active_users as [varname] %}
        {% active_users %}

    Example usage::
        {% load request_tag %}
        {% active_users in 10 minutes as user_list %}
        {% for user in user_list %}
            {{ user.username }}
        {% endfor %}
    """
    return ActiveUserNode(parser, token)
