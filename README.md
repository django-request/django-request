django-request
==============

[![Build Status](https://github.com/django-request/django-request/workflows/Tests/badge.svg?branch=master)](https://github.com/django-request/django-request/actions)
[![Coverage Status](https://coveralls.io/repos/github/django-request/django-request/badge.svg?branch=master)](https://coveralls.io/github/django-request/django-request?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/django-request.svg)](https://pypi.org/project/django-request/)

django-request is a statistics module for django. It stores requests in a database for admins to see, it can also be used to get statistics on who is online etc.

![Traffic graph](docs/graph.png)

As well as a site statistics module, with the `active_users` template tag and manager method you can also use django-request to show who is online in a certain time.

    Request.objects.active_users(minutes=15)

To find the request overview page, please click on Requests inside the admin, then “Overview” on the top right, next to “add request”.

Requirements
------------

* **Python**: 3.6, 3.7, 3.8, 3.9, 3.10
* **Django**: 2.2, 3.2, 4.0
* **python-dateutil**

django-request [1.5.1](https://pypi.org/project/django-request/1.5.1/) is the last version that supports Django 1.4, 1.5, 1.6.

django-request [1.5.4](https://pypi.org/project/django-request/1.5.4/) is the
last version that supports Django 1.7, 1.8, 1.9.

django-request [1.5.5](https://pypi.org/project/django-request/1.5.5/) is the
last version that supports Django 1.10.

django-request [1.5.6](https://pypi.org/project/django-request/1.5.5/) is the
last version that supports Django 1.11, 2.0, 2.1, 3.0, 3.1, and Python 2.7 and
3.4.

Installation
------------

- Put `'request'` in your `INSTALLED_APPS` setting.
- Run the command `manage.py migrate`.
- Add `request.middleware.RequestMiddleware` to `MIDDLEWARE`. If you use `django.contrib.auth.middleware.AuthenticationMiddleware`, place the `RequestMiddleware` after it. If you use `django.contrib.flatpages.middleware.FlatpageFallbackMiddleware` place `request.middleware.RequestMiddleware` before it else flatpages will be marked as error pages in the admin panel.
- Add `REQUEST_BASE_URL` to your settings with the base URL of your site (e.g.
  `https://www.my.site/`). This is used to calculate unique visitors and top
  referrers. `REQUEST_BASE_URL` defaults to
  `'http://%s' % Site.objects.get_current().domain`.

Detailed documentation
----------------------

For a detailed documentation of django-request, or how to install django-request please see: [django-request](https://django-request.readthedocs.org/en/latest/) or the docs/ directory.
