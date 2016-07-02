# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status

from .base import BaseAPITestCase


class BaseInfrastructureTestCase(BaseAPITestCase):

    def test_404(self):
        response = self.make_get_request(url='/missing/endpoint')

        self.assert_response_error(response, 'not_found', status.HTTP_404_NOT_FOUND)
