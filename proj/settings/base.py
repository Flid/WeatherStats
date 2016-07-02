# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from .log import LOGGING

ALLOWED_HOSTS = ['*']

PRODUCTION = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_dir = lambda x: os.path.join(BASE_DIR, x)

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
