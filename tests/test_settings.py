import django

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
    'other': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

SECRET_KEY = 'django_requests_tests_secret_key'

# Use a fast hasher to speed up tests.
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.admin',
    'tests',
    'request',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

# Old-style middleware using settings.MIDDLEWARE_CLASSES is deprecated since django 1.10
if django.VERSION >= (1, 10):
    MIDDLEWARE = MIDDLEWARE_CLASSES
    del MIDDLEWARE_CLASSES

STATIC_URL = '/static/'

ROOT_URLCONF = 'tests.test_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ],
        },
    },
]
