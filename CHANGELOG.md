# Changelog for django-request

## 1.6.3

### Enhancements

* Confirms support for Django 4.2.

### Bug Fixes

* Adds a missing migration with HTTP status codes.

## 1.6.2

### Enhancements

* Adds support for missing HTTP status codes: 103, 208, 226, 308, 428, 429,
  431, 451, and 511.

* Confirms support for Python 3.11.

* Confirms support for Django 4.1.

* Don't ignore [boosted htmx requests](https://htmx.org/attributes/hx-boost/)
  with ``REQUEST_IGNORE_AJAX``.

## 1.6.1

### Enhancements

* Adds warning logging to middleware on invalid IP addresses in
  ``REMOTE_ADDR``.

### Bug Fixes

* Adds a missing migration to change ``help_text`` of ``Request.is_ajax``.

## 1.6.0

### Breaking

* Support for Django 1.11, 2.0, 2.1, 3.0, and 3.1 has been dropped.

* Support for Python 2.7 and 3.4 has been dropped.

### Enhancements

* Adds [htmx](https://htmx.org/) support to the ``REQUEST_IGNORE_AJAX``
  setting.

* Confirms support for Django 4.0.

* Confirms support for Django 3.2.

* Confirms support for Python 3.10.

* Confirms support for Python 3.9.

### Bug Fixes

* Fixes middleware crash on invalid IP addresses in ``REMOTE_ADDR``.

## 1.5.6.

### Breaking

* Support for Django 1.10 has been dropped.

### Enhancements

* Confirms support for Python 3.8.

* Confirms support for Python 3.7.

* Adds support for Django 3.1.

* Confirms support for Django 3.0.

* Confirms support for Django 2.2.

### Bug Fixes

* Fixes a performance regression in the admin's requests overview (#200).

* Fixes handling naive datetimes in the admin's requests overview.

## 1.5.5.

### Breaking

* Support for Django 1.7-1.9 has been dropped.

### Bug Fixes

* Fixes series of dates in a _Traffic Graph_ in the admin's requests overview
  (#180).

* Fixes crash of ``Modules.graph()`` when Django's translation is disabled i.e.
  ``USE_I18N = False`` (#168).
