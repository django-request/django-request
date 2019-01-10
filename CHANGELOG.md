# Changelog for django-request

## 1.5.5.

### Breaking

* Support for Django 1.7-1.9 has been dropped.

### Bug Fixes

* Fixes series of dates in a _Traffic Graph_ in the admin's requests overview
  (#180).

* Fixes crash of ``Modules.graph()`` when Django's translation is disabled i.e.
  ``USE_I18N = False`` (#168).
