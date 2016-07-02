# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *  # nopep8

SECRET_KEY = 'test_secret_key_string'

HOSTNAME = 'api.example.com'

TESTING = True
DEBUG = False

WEATHER_API_KEY = 'fake_value'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'weather_stats.db',
    },
}

STATIC_ROOT = '/var/www/static/'
