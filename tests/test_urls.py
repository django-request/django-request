# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)
