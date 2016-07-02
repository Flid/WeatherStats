# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/', include('weather_stats.urls', namespace='weather_stats')),
    url(r'', include('rest_framework_swagger.urls')),
]

handler400 = 'weather_stats.views.custom_400_handler'
handler403 = 'weather_stats.views.custom_403_handler'
handler404 = 'weather_stats.views.custom_404_handler'
handler500 = 'weather_stats.views.custom_500_handler'
