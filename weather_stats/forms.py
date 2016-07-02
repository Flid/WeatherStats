# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from weather_stats import validators as v


class WeatherStatsShowForm(v.Schema):
    location = v.String(
        not_empty=True,
        description='Any query string, like `london`.',
    )

    date_start = v.Pipeline(
        v.DateConverter(),
        # Pass callable here, so date is reevaluated every time
        v.DateValidator(latest_date=date.today),
        description='Starting date to query. Format: mm/dd/yyyy',
    )
    date_end = v.Pipeline(
        v.DateConverter(),
        v.DateValidator(latest_date=date.today),
        description='Closing date to query. Format: mm/dd/yyyy. '
                    'Should be less than `date_start`',
    )

    chained_validators = [
        v.GTEValidator(
            name_less='date_start',
            name_greater='date_end',
        ),
    ]
