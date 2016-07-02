# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import BaseApiView
from rest_framework.response import Response


class ReadStatsView(BaseApiView):

    def get(self, request):
        return Response()
