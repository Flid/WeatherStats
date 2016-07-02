# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from .log import LOGGING

ALLOWED_HOSTS = ['*']

PRODUCTION = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'proj.urls'

TIME_ZONE = u'Europe/London'
LANGUAGE_CODE = u'en-GB'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Application definition

INSTALLED_APPS = [
    b'django.contrib.auth',
    b'django.contrib.contenttypes',
    b'django.contrib.sessions',
    b'django.contrib.sites',
    b'django.contrib.staticfiles',
    b'django.contrib.messages',
    b'rest_framework',
    b'rest_framework_swagger',
    b'weather_stats',
]


MIDDLEWARE_CLASSES = [
    b'django.contrib.sessions.middleware.SessionMiddleware',
    b'django.middleware.common.CommonMiddleware',
    b'django.middleware.csrf.CsrfViewMiddleware',
    b'django.contrib.auth.middleware.AuthenticationMiddleware',
    b'django.contrib.messages.middleware.MessageMiddleware',
    b'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

WSGI_APPLICATION = 'proj.wsgi.application'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        b'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        b'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'EXCEPTION_HANDLER': b'weather_stats.utils.exception_handler',

    'COMPACT_JSON': False,
}

STATIC_URL = '/static/'
STATIC_ROOT = ''

SITE_ID = 1


SWAGGER_SETTINGS = {
    'api_version': '1',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'resource_access_handler': None,
    'base_path': 'weather-stats.com',
    'info': {
        'title': 'Weather Stats API',
    },
    'doc_expansion': 'full',
}
