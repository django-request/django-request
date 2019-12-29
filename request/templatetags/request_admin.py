# -*- coding: utf-8 -*-
from django import template
from django.utils.http import quote

register = template.Library()


@register.simple_tag
def pie_chart(items, width=440, height=190):
    return '//chart.googleapis.com/chart?cht=p3&chd=t:{0}&chs={1}x{2}&chl={3}'.format(
        quote(','.join([str(item[1]) for item in items])),
        width,
        height,
        quote('|'.join([str(item[0]) for item in items])),
    )
