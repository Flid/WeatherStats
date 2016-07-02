# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import Mock, patch
from rest_framework import status

from .base import BaseAPITestCase

TEST_LOCATION = 'London'
TEST_DATE_START = '01/01/2016'
TEST_DATE_END = '01/02/2016'


class StatsViewTestCase(BaseAPITestCase):
    default_url = '/api/stats/read'

    def setUp(self):
        super(StatsViewTestCase, self).setUp()

        self.api_client_mock = Mock(return_value={
            'location': 'London, United Kingdom',
            'days': [
                {
                    'pressure': 1020,
                    'date_str': '2016-01-01',
                    'temperature': 8,
                    'humidity': 77,
                },
                {
                    'pressure': 998,
                    'date_str': '2016-01-02',
                    'temperature': 10,
                    'humidity': 80,
                },
            ],
        })

        self.api_client_patch = patch(
            'weather_stats.weather_api.WeatherHistoryAPI.get_history_data',
            self.api_client_mock,
        )

        self.api_client_patch.start()

    def tearDown(self):
        self.api_client_patch.stop()
        super(StatsViewTestCase, self).tearDown()

    def get_args(self, **kwargs):
        default_args = {
            'location': TEST_LOCATION,
            'date_start': TEST_DATE_START,
            'date_end': TEST_DATE_END,
        }
        default_args.update(kwargs)

        return {k: v for k, v in default_args.iteritems() if v is not None}

    def test_simple(self):
        response = self.make_get_request(query_args=self.get_args())

        data = self.assert_response_ok(response)

        self.assertEqual(data, {
            'location': 'London, United Kingdom',
            'humidity': {'average': 78, 'max': 80, 'median': 80, 'min': 77},
            'pressure': {'average': 1009, 'max': 1020, 'median': 1020, 'min': 998},
            'temperature': {'average': 9, 'max': 10, 'median': 10, 'min': 8},
        })

    def test_without_args(self):
        response = self.make_get_request()

        self.assert_response_error(
            response,
            'invalid_args',
            errors=['date_end.empty', 'date_start.empty', 'location.empty'],
        )

    def test_invalid_date_format(self):
        for date_start in ['abc', '1/1/1', '1-3-4', '20/20/2016']:
            response = self.make_get_request(
                query_args=self.get_args(date_start=date_start),
            )

            self.assert_response_error(
                response,
                'invalid_args',
                errors=['date_start.invalid'],
            )

    def test_end_date_less_than_start_date(self):
        response = self.make_get_request(
            query_args=self.get_args(date_start=TEST_DATE_END, date_end=TEST_DATE_START),
        )

        self.assert_response_error(
            response,
            'invalid_args',
            errors=['date_end.invalid'],
        )

    def test_unicode_symbols(self):
        response = self.make_get_request(
            query_args=self.get_args(location='場所'),
        )
        self.assert_response_ok(response)

    def test_internal_error(self):
        self.api_client_mock.side_effect = ValueError

        response = self.make_get_request(query_args=self.get_args())

        self.assert_response_error(
            response,
            'internal',
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
