# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from rest_framework import exceptions as rest_exceptions
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    is_server_error,
)

from weather_stats.exceptions import BaseApiError
from weather_stats.types import DataWithStatus

logger = logging.getLogger(__name__)

REST_EXCEPTIONS_TO_CODES = {
    rest_exceptions.AuthenticationFailed: 'auth_failed',
    rest_exceptions.NotAuthenticated: 'auth_not_provided',
    rest_exceptions.PermissionDenied: 'permission_denied',
    rest_exceptions.MethodNotAllowed: 'method_not_allowed',
}


def exception_handler(exc, context):
    """
    When error is raised inside API view, it will be processed by this function.

    :param exc: Exception to process.
    :return: Response with error JSON.
    """
    response_data = {'error_code': 'internal'}
    status = HTTP_500_INTERNAL_SERVER_ERROR

    if isinstance(exc, BaseApiError):
        response_data.update(exc.format_exc())
        status = exc.status_code

    if is_server_error(status):
        logger.critical('Internal API exception', exc_info=exc)
        if settings.DEBUG:
            raise

    logging.info(
        'Error response. status_code=%s, error_code=%s',
        status,
        response_data['error_code'],
    )

    return Response(
        DataWithStatus('error', **response_data),
        status=status,
    )
