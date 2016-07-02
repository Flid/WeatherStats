# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import sys

from django.conf import settings
from django.http import Http404, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import APIException

from weather_stats import exceptions as api_exceptions

logger = logging.getLogger(__name__)


class BaseApiView(GenericAPIView):
    # A list of forms for the current view. Format:
    # {b'GET': Form, b'POST': [Form1, Form2], ...}
    form_class = None

    def initial(self, request, *args, **kwargs):
        logger.info(
            'New request: %s %s://%s%s',
            request.method,
            request.scheme,
            request.get_host(),
            request.get_full_path(),
        )
        super(BaseApiView, self).initial(request, *args, **kwargs)
        self.validate_forms()

    def validate_forms(self):
        """
        Process input args, put results into `self.form_values`
        """

    def get_renderer_context(self):
        context = super(BaseApiView, self).get_renderer_context()

        # Pretty-print JSON by default.
        context['indent'] = 2
        return context


def custom_error_handler(status_code, error_code):
    def handler(request, **kwargs):
        exc = sys.exc_info()[1]
        log_method = logging.info if isinstance(exc, APIException) else logging.exception

        log_method(
            'Error response. status_code=%s, error_code=%s',
            status_code,
            error_code,
        )
        return JsonResponse(
            {'status': 'error', 'error_code': error_code},
            status=status_code,
        )

    return handler


custom_400_handler = custom_error_handler(400, 'bad_request')
custom_403_handler = custom_error_handler(403, 'permission_denied')
custom_404_handler = custom_error_handler(404, 'not_found')
custom_500_handler = custom_error_handler(500, 'internal')
