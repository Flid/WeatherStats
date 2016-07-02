# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import sys

from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView

from weather_stats import exceptions as api_exceptions
from weather_stats.validators import Invalid

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
        Check all the data according to forms set,
        put all the validated data to `self.form_values`.
        """
        assert self.form_class

        self.form_values = {}

        logger.info('Processing form %s', self.form_class)
        logger.debug('Input args: %s', self.request.GET)

        try:
            self.form_values.update(
                self.form_class().to_python(self.request.GET),
            )
        except Invalid as ex:
            raise api_exceptions.ValidationFailedError(
                ex,
                detail='Input args validation failed. Check your request.',
            )

        logger.info('Forms have been processed successfully.')

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
