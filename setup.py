#!/usr/bin/env python
import request
from setuptools import setup

setup(
    name='django-request',
    version=request.__version__,
    description=open('docs/description.txt').read(),
    long_description=open('docs/long_description.txt').read(),
    author='Kyle Fuller',
    author_email='kyle@fuller.li',
    url=request.__URL__,
    download_url='https://github.com/django-request/django-request/archive/{0}.zip'.format(request.__version__),
    packages=[
        'request',
        'request.migrations',
        'request.templatetags',
        'request.management',
        'request.management.commands',
    ],
    package_data={'request': [
        'templates/admin/request/*.html',
        'templates/admin/request/request/*.html',
        'templates/request/plugins/*.html',
        'static/request/js/*.js',
        'locale/*/LC_MESSAGES/*.*',
    ]},
    install_requires=[
        'django >= 1.4',
        'python-dateutil',
    ],
    license=request.__licence__,
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
