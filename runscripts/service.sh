#!/usr/bin/env bash
(gunicorn gmailcron.wsgi --bind 0.0.0.0:8000 --workers 2 --timeout 0 --log-level=debug) 
