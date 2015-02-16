#!/bin/sh
uwsgi --http :8888 --chdir ./weather_app --pp ./weather_app -w weather_app.wsgi
