from django import template

register = template.Library()


def trunc(string, chars):
    if len(string) > int(chars):
        return "%s..." % string[:int(chars) - 3]
    return string
register.filter('trunc', trunc)


def pie_chart(items, width=440, height=190):
    return '//chart.googleapis.com/chart?cht=p3&chd=t:%s&chs=%sx%s&chl=%s' % (
        ','.join([str(item[1]) for item in items]),
        width,
        height,
        '|'.join([str(item[0]) for item in items])
    )
register.simple_tag(pie_chart)
