#!/usr/bin/env python
from distutils.core import setup
import request

setup(
    name='django-request',
    version='%s' % request.__version__,
    description='django-request is a statistics module for django. It stores requests in a database for admins to see, it can also be used to get statistics on who is online etc.',
    author='Kyle Fuller',
    author_email='inbox@kylefuller.co.uk',
    url='http://kylefuller.co.uk/projects/django-request/',
    download_url='http://github.com/kylef/django-request/zipball/%s' % request.__version__,
    packages=['request', 'request.templatetags'],
    package_data={'request': ['templates/admin/request/*.html', 'templates/admin/request/request/*.html']},
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
