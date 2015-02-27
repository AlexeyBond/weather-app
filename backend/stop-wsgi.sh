#!/bin/sh
kill -SIGINT `cat /tmp/weatherapp-uwsgi-master.pid`
