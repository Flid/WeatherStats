# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class DataWithStatus(dict):
    """
    A simple structure, that indicates that the response is already processed.
    """
    def __init__(self, status, data=None, **kwargs):
        super(DataWithStatus, self).__init__(status=status, **kwargs)
        if data is not None:
            self['data'] = data
