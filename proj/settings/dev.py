# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .test import *  # nopep8
SECRET_KEY = 'test_secret_key_string'

WEATHER_API_KEY = '0b970d98300c4073b81105623160207'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'weather_stats.db',
    },
}
