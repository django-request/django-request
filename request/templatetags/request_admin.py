from django import template

register = template.Library()

#@register.tag
def trunc(string, chars):
    if len(string) > int(chars):
        return "%s..." % string[:int(chars)-3]
    else:
        return string
register.filter('trunc', trunc)