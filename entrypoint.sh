#!/bin/sh
pwd
ls -lah
ls -lah /code/pitmarket_root
cd pitmarket_root
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn pitmarket_site.wsgi:application --bind 0.0.0.0:8000 --log-level debug --timeout 10 --workers 4

