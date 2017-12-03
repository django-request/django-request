django-request
==============

[![Build Status](http://img.shields.io/travis/django-request/django-request/master.svg?style=flat)](https://travis-ci.org/django-request/django-request)
[![Coverage Status](https://coveralls.io/repos/github/django-request/django-request/badge.svg?branch=master)](https://coveralls.io/github/django-request/django-request?branch=master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/django-request.svg)](https://pypi.python.org/pypi/django-request)
[![PyPI Version](https://img.shields.io/pypi/v/django-request.svg)](https://pypi.python.org/pypi/django-request)

django-request is a statistics module for django. It stores requests in a database for admins to see, it can also be used to get statistics on who is online etc.

![Traffic graph](docs/graph.png)

As well as a site statistics module, with the `active_users` template tag and manager method you can also use django-request to show who is online in a certain time.

    Request.objects.active_users(minutes=15)

To find the request overview page, please click on Requests inside the admin, then “Overview” on the top right, next to “add request”.

Requirements
------------

* **Python**: 2.7, 3.4, 3.6
* **Django**: 1.7, 1.8, 1.9, 1.10, 1.11, 2.0
* **python-dateutil**

django-request [1.5.1](https://pypi.python.org/pypi/django-request/1.5.1) is the last version that supports Django 1.4, 1.5, 1.6.

Installation
------------

- Put `'request'` in your `INSTALLED_APPS` setting.
- Run the command `manage.py migrate`.
- Add `request.middleware.RequestMiddleware` to `MIDDLEWARE`. If you use `django.contrib.auth.middleware.AuthenticationMiddleware`, place the `RequestMiddleware` after it. If you use `django.contrib.flatpages.middleware.FlatpageFallbackMiddleware` place `request.middleware.RequestMiddleware` before it else flatpages will be marked as error pages in the admin panel.
- Make sure that the domain name in `django.contrib.sites` admin is correct. This is used to calculate unique visitors and top referrers.

Detailed documentation
----------------------

For a detailed documentation of django-request, or how to install django-request please see: [django-request](https://django-request.readthedocs.org/en/latest/) or the docs/ directory.
