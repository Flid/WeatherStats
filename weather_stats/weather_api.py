# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import requests
from django.conf import settings
from furl import furl
from requests.exceptions import RequestException

from weather_stats.exceptions import WeatherAPIException

log = logging.getLogger(__name__)


class WeatherHistoryAPI(object):
    """
    Official client is outdated (3 years without changes)
    and doesn't seem to work. THat's why we need this tiny client.
    """
    BASE_URL = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx'
    DATE_FORMAT = '%Y-%m-%d'

    def _process_raw_data(self, data):
        """
        Remove unneeded data and reformat the output a bit.
        """
        output = {
            'location': data['data']['request'][0]['query'],
            'days': [],
        }

        for day in data['data']['weather']:
            output['days'].append({
                'temp_min': int(day['mintempC']),
                'temp_max': int(day['maxtempC']),
                'humidity': int(day['hourly'][0]['humidity']),
                'date_str': day['date'],
            })

        return output

    def get_history_data(self, location, date_start, date_end):
        url = furl(self.BASE_URL)

        url.args.update({
            'q': location,
            'date': date_start.strftime(self.DATE_FORMAT),
            'enddate': date_end.strftime(self.DATE_FORMAT),
            'key': settings.WEATHER_API_KEY,
            'tp': '24',
            'format': 'json',
        })

        try:
            response = requests.get(str(url))
            data = response.json()
        except (RequestException, ValueError) as ex:
            log.error('Failed to read weather api', exc_info=ex)
            raise WeatherAPIException()

        try:
            return self._process_raw_data(data)
        except KeyError as ex:
            log.error('Failed to parse weather api response: %s', data, exc_info=ex)
            raise WeatherAPIException()
