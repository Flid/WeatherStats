# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


class BaseAPITestCase(TestCase):
    pass


class BaseUnitTestCase(TestCase):
    maxDiff = None
