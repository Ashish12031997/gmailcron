#!/usr/bin/env bash
service supervisor start
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
(gunicorn smart_mail_management.wsgi --bind 0.0.0.0:8000 --workers 2 --timeout 0 --log-level=debug) &
sleep 10 &
tail -F ./logs/info.log ./logs/error.log
