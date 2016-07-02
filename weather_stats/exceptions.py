# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import exceptions as rest_exceptions
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class BaseApiError(rest_exceptions.APIException):
    """
    Basic exception class, never raise it directly!
    """
    code = None
    default_detail = None

    def __init__(self, detail=None):
        self.detail = detail

    def format_exc(self):
        error_data = {'error_code': self.code}

        detail = self.detail or self.default_detail
        if detail is not None:
            error_data['message'] = detail

        return error_data


class NotFoundError(BaseApiError):
    code = '%s.not_found'
    status_code = HTTP_404_NOT_FOUND

    def __init__(self, obj_name, detail=None):
        super(NotFoundError, self).__init__(detail=detail)

        self.obj_name = obj_name

    def format_exc(self):
        error_data = super(NotFoundError, self).format_exc()
        error_data['error_code'] %= self.obj_name.lower()
        return error_data


class InternalApiError(BaseApiError):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    code = 'internal'
