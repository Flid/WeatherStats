# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response

from weather_stats.forms import WeatherStatsShowForm
from weather_stats.weather_api import WeatherHistoryAPI

from .base import BaseApiView


class ReadStatsView(BaseApiView):
    """
    Calculate min/max/average/median temperature/humidity/pressure
    for a given location over some period of time.
    """
    form_class = WeatherStatsShowForm

    def get(self, request):
        self.validate_forms()

        weather_data = WeatherHistoryAPI().get_history_data(
            self.form_values['location'],
            self.form_values['date_start'],
            self.form_values['date_end'],
        )

        def _get_stats(param_name):
            values = [item[param_name] for item in weather_data['days']]

            return {
                'min': min(values),
                'max': max(values),
                'average': sum(values) / len(values),
                'median': sorted(values)[len(values) / 2],
            }

        response_data = {
            'temperature': _get_stats('temperature'),
            'pressure': _get_stats('pressure'),
            'humidity': _get_stats('humidity'),
            'location': weather_data['location'],
        }

        # Well, we can use DRF serializers here, but it makes no sense.
        return Response(response_data)
