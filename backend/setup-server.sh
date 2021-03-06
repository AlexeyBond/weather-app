#!/bin/sh

# Скрипт установки всех необходимых пакетов для запуска сервера.

###################################################################
# Должен быть запущен из текущей папки от имени сиперпользователя #
#     на системе под управлением Ubuntu>=12.04, со стабильным     #
#      подключением к сети "Интернет" бородатым сисадмином в      #
#      четвёртые лунные сутки при спокойной погоде на марсе       #
###################################################################

apt-get install nginx
apt-get install python python-pip
pip install flask
pip install uwsgi

mkdir /srv/www
ln -s -T "$PWD/../frontend" /srv/www/frontend
cp ./nginx-settings /etc/nginx/sites-enabled/weather-app
