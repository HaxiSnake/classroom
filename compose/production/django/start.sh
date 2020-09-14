#!/bin/bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn classroom.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/app 
