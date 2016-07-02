# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from weather_stats import validators as v


class WeatherStatsShowForm(v.Schema):
    location = v.String(not_empty=True)

    date_start = v.ParsingDateValidator
    date_end = v.ParsingDateValidator

    chained_validators = [
        v.GTEValidator(
            name_less='date_start',
            name_greater='date_end',
        ),
    ]
