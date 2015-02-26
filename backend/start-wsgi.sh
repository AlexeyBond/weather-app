#!/bin/sh
uwsgi --http :8888 --pp . -w weather_app.app --callable app
