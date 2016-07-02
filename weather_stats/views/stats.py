# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response

from weather_stats.forms import WeatherStatsShowForm
from weather_stats.weather_api import WeatherHistoryAPI

from .base import BaseApiView


class ReadStatsView(BaseApiView):
    form_class = WeatherStatsShowForm

    def get(self, request):
        self.validate_forms()

        weather_data = WeatherHistoryAPI().get_history_data(
            self.form_values['location'],
            self.form_values['date_start'],
            self.form_values['date_end'],
        )

        return Response(weather_data)
