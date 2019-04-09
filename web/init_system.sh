#!/usr/bin/env bash
cd /app
python manage.py collectstatic --noinput
#python manage.py makemigrations
python manage.py makemigrations garage
python manage.py migrate
python manage.py createsuperuser
