#!/usr/bin/env python
import os
import sys
import warnings

import django

if __name__ == "__main__":
    warnings.simplefilter("always", DeprecationWarning)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')

    if hasattr(django, "setup"):
        django.setup()

    try:
        from django.test.runner import DiscoverRunner as TestRunner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner as TestRunner

    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))
