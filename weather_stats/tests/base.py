# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
from django.test import TestCase
from rest_framework import status


class BaseAPITestCase(TestCase):
    default_url = None

    def make_get_request(self, url=None, query_args=None):
        url = url or self.default_url

        return self.client.get(url, data=query_args)

    def extract_response_data(self, response):
        if isinstance(response, JsonResponse):
            return json.loads(response.content)

        return response.data

    def assert_response_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(data['status'], 'ok')

        return data['data']

    def assert_response_error(self, response, code, status=status.HTTP_400_BAD_REQUEST,
                              **kwargs):
        data = self.extract_response_data(response)

        self.assertEqual(response.status_code, status, [response.status_code, data])

        self.assertTrue(isinstance(data, dict), data)
        self.assertEqual(data.get('status'), 'error')
        self.assertEqual(
            data.get('error_code'),
            code,
            'Expected code is %s, received that data instead: %s' % (code, data),
        )
        for key, value in kwargs.iteritems():
            self.assertEqual(data[key], value, [key, data[key], value])

        return data


class BaseUnitTestCase(TestCase):
    maxDiff = None
