#!/usr/bin/env bash
celery -A  smart_mail_management beat -l info -f logs/info.log
