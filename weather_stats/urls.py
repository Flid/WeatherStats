# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from weather_stats.views import stats as stats_views

urlpatterns = [
    url(r'^stats/read$', stats_views.ReadStatsView.as_view()),
]
