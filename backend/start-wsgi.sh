#!/bin/sh
uwsgi --master --pidfile /tmp/weatherapp-uwsgi-master.pid --http :8888 --pp . -w weather_app.app --callable app
