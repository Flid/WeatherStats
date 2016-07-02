# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test.utils import override_settings
from furl import furl
from mock import Mock, patch
from requests.exceptions import HTTPError

from weather_stats.exceptions import WeatherAPIException
from weather_stats.weather_api import WeatherHistoryAPI

from .base import BaseUnitTestCase

# Snapshot of API response
TEST_RESPONSE = {
    'data': {
        'weather': [
            {
                'mintempC': '7',
                'maxtempF': '46',
                'mintempF': '44',
                'maxtempC': '8',
                'hourly': [
                    {
                        'windspeedKmph': '33',
                        'FeelsLikeF': '40',
                        'winddir16Point': 'ESE',
                        'FeelsLikeC': '5',
                        'DewPointC': '5',
                        'windspeedMiles': '21',
                        'DewPointF': '40',
                        'HeatIndexF': '47',
                        'cloudcover': '100',
                        'HeatIndexC': '8',
                        'precipMM': '0.7',
                        'weatherIconUrl': [
                            {'value': 'http://example.com/imagepng'},
                        ],
                        'WindGustMiles': '21',
                        'pressure': '1020',
                        'WindGustKmph': '35',
                        'weatherDesc': [{'value': 'Overcast '}],
                        'visibility': '10',
                        'weatherCode': '122',
                        'tempC': '8',
                        'tempF': '46',
                        'WindChillF': '40',
                        'WindChillC': '5',
                        'winddirDegree': '113',
                        'humidity': '77',
                        'time': '24',
                    },
                ],
                'date': '2016-01-01',
                'astronomy': [
                    {
                        'moonrise': 'No moonrise',
                        'moonset': '12:25 PM',
                        'sunset': '05:02 PM',
                        'sunrise': '09:06 AM',
                    },
                ],
                'uvIndex': '0',
            },
            {
                'mintempC': '2',
                'maxtempF': '51',
                'mintempF': '36',
                'maxtempC': '10',
                'hourly': [
                    {
                        'windspeedKmph': '40',
                        'FeelsLikeF': '46',
                        'winddir16Point': 'SSE',
                        'FeelsLikeC': '8',
                        'DewPointC': '8',
                        'windspeedMiles': '25',
                        'DewPointF': '46',
                        'HeatIndexF': '52',
                        'cloudcover': '99',
                        'HeatIndexC': '11',
                        'precipMM': '4.6',
                        'weatherIconUrl': [
                            {'value': 'http://example.com/image.png'},
                        ],
                        'WindGustMiles': '31',
                        'pressure': '998',
                        'WindGustKmph': '50',
                        'weatherDesc': [{'value': 'Patchy rain nearby'}],
                        'visibility': '10',
                        'weatherCode': '176',
                        'tempC': '10',
                        'tempF': '51',
                        'WindChillF': '46',
                        'WindChillC': '8',
                        'winddirDegree': '158',
                        'humidity': '80',
                        'time': '24',
                    },
                ],
                'date': '2016-01-02',
                'astronomy': [
                    {
                        'moonrise': '01:02 AM',
                        'moonset': '12:48 PM',
                        'sunset': '05:03 PM',
                        'sunrise': '09:06 AM',
                    },
                ],
                'uvIndex': '0',
            },
        ],
        'request': [
            {'query': 'London, United Kingdom', 'type': 'City'},
        ],
    },
}

WEATHER_API_KEY = 'some_key_value'


@override_settings(
    WEATHER_API_KEY=WEATHER_API_KEY,
)
class HistoryDataTestCase(BaseUnitTestCase):
    def setUp(self):
        super(HistoryDataTestCase, self).setUp()

        self.response_mock = Mock(json=Mock(return_value=TEST_RESPONSE))
        self.requests_get_mock = Mock(return_value=self.response_mock)

        self.request_patch = patch(
            'requests.get',
            self.requests_get_mock,
        )
        self.request_patch.start()

        self.api_client = WeatherHistoryAPI()

    def tearDown(self):
        self.request_patch.stop()
        super(HistoryDataTestCase, self).tearDown()

    def test_simple(self):

        response = self.api_client.get_history_data(
            'london',
            date(2016, 1, 1),
            date(2016, 1, 2),
        )

        self.assertEqual(
            response,
            {
                'location': 'London, United Kingdom',
                'days': [
                    {
                        'date_str': '2016-01-01',
                        'temperature': 8,
                        'humidity': 77,
                        'pressure': 1020,
                    },
                    {
                        'date_str': '2016-01-02',
                        'temperature': 10,
                        'humidity': 80,
                        'pressure': 998,
                    },
                ],
            },
        )

        self.assertEqual(self.requests_get_mock.call_count, 1)

        url = furl(self.requests_get_mock.call_args_list[0][0][0])

        self.assertTrue(str(url).startswith(WeatherHistoryAPI.BASE_URL))
        self.assertEqual(
            url.args,
            {
                'q': 'london',
                'date': '2016-01-01',
                'enddate': '2016-01-02',
                'key': WEATHER_API_KEY,
                'tp': '24',
                'format': 'json',
            },
        )

    def test_request_error(self):
        self.requests_get_mock.side_effect = HTTPError

        with self.assertRaises(WeatherAPIException):
            self.api_client.get_history_data(
                'london',
                date(2016, 1, 1),
                date(2016, 1, 2),
            )

    def test_parse_error(self):
        self.response_mock.json.return_value = {}

        with self.assertRaises(WeatherAPIException):
            self.api_client.get_history_data(
                'london',
                date(2016, 1, 1),
                date(2016, 1, 2),
            )
