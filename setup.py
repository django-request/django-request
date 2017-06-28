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
    maintainer='Mariusz Felisiak',
    maintainer_email='felisiak.mariusz@gmail.com',
    url=request.__URL__,
    download_url='https://pypi.python.org/pypi/django-request',
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
        'Django>=1.7',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
    ],
)
