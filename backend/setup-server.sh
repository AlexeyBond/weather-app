#!/bin/sh

apt-get install nginx
apt-get install python python-pip
pip install django
pip install uwsgi

mkdir /srv/www
ln -s -T "$PWD/../frontend" /srv/www/frontend
cp ./nginx-settings /etc/nginx/sites-enabled/weather-app
