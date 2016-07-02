# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import exceptions as rest_exceptions
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)


class BaseApiError(rest_exceptions.APIException):
    """
    Basic exception class, never raise it directly!
    """
    code = None
    default_detail = None

    def __init__(self, detail=None):
        self.detail = detail


class InternalApiError(BaseApiError):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    code = 'internal'


class ValidationFailedError(BaseApiError):
    """Validation form error"""
    status_code = HTTP_400_BAD_REQUEST
    code = 'invalid_args'

    DEFAULT_REASON = 'invalid'

    CODE_TO_REASON = {
        'empty': 'empty',
        'missingValue': 'empty',
    }

    def __init__(self, invalid_exception, *args, **kwargs):
        self._invalid_exception = invalid_exception
        super(ValidationFailedError, self).__init__(*args, **kwargs)

    def format_exc(self):
        errors, details = self._flatten_exception(self._invalid_exception)
        error_data = {
            'error_code': self.code,
            'errors': errors,
            'details': details,
        }

        detail = self.detail or self.default_detail
        if detail is not None:
            error_data['message'] = detail

        return error_data

    def _format_error_code(self, exc, field):
        code = getattr(exc, 'code', None)
        reason = self.CODE_TO_REASON.get(code, self.DEFAULT_REASON)
        return '%s.%s' % (field, reason)

    def _flatten_internal(self, exc, details, field=None):
        errors = set()

        for field, e in (exc.error_dict or {}).iteritems():
            errors.update(self._flatten_internal(e, details, field))

        if not errors:
            error_code = self._format_error_code(exc, field)
            if exc.msg:
                details[error_code] = exc.msg
            errors.add(error_code)

        return errors

    def _flatten_exception(self, exc):
        """Convert the complicated errors structure to a flat list."""
        details = {}
        return sorted(list(self._flatten_internal(exc, details))), details


class WeatherAPIException(BaseApiError):
    code = 'external_api.failed'
    status_code = HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Error while calling external service'
