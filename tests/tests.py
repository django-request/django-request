# -*- coding: utf-8 -*-
import django

if django.VERSION < (1, 6):
    from .test_admin import *
    from .test_command import *
    from .test_managers import *
    from .test_middlewares import *
    from .test_models import *
    from .test_plugins import *
    from .test_router import *
    from .test_templatestags import *
    from .test_traffic import *
    from .test_urls import *
