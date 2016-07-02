#!/bin/bash

if [ -z "$COV_OPTS" ];
  then
    COV_OPTS="--cov --cov-config=.coveragerc --cov-report html --cov-report term-missing"
fi

if [ -z "$OPTS" ];
  then
    OPTS="--nomigrations --reuse-db"
fi

if [[ $# -eq 0 ]] || [[ $1 == -* ]]
  then
    DJANGO_SETTINGS_MODULE=proj.settings.test ./ve/bin/py.test $OPTS $COV_OPTS ./weather_stats/tests/ $@
  else
    DJANGO_SETTINGS_MODULE=proj.settings.test ./ve/bin/py.test $OPTS $@
fi
