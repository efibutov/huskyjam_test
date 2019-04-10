#!/usr/bin/env bash
cd /app
python manage.py collectstatic --noinput
rm -rf /app/garage/migrations
python manage.py makemigrations garage
python manage.py migrate
python manage.py createsuperuser
