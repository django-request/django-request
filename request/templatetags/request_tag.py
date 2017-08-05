# -*- coding: utf-8 -*-
from django import template

from ..models import Request

register = template.Library()


class ActiveUserNode(template.Node):
    def __init__(self, parser, token):
        tokens = token.contents.split()
        tag_name = tokens.pop(0)
        self.kwargs = {}
        self.as_varname = 'user_list'

        if len(tokens) not in (5, 2, 0):
            raise template.TemplateSyntaxError('Incorrect amount of arguments in the tag {0!r}'.format(tag_name))

        if len(tokens) == 5 and tokens[0] == 'in':
            tokens.pop(0)  # pop 'in' of tokens
            try:
                self.kwargs[str(tokens.pop(0))] = int(tokens.pop(0))
            except ValueError:
                raise template.TemplateSyntaxError('Invalid arguments for {0!r} template tag.'.format(tag_name))
        else:
            self.kwargs['minutes'] = 15

        if len(tokens) == 2 and tokens[0] == 'as':
            self.as_varname = tokens[1]

    def render(self, context):
        context[self.as_varname] = Request.objects.active_users(**self.kwargs)
        return ''


@register.tag
def active_users(parser, token):
    '''
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
            {{ user.get_username }}
        {% endfor %}
    '''
    return ActiveUserNode(parser, token)
