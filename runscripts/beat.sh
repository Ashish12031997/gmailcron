#!/usr/bin/env bash
celery -A  gmailcron beat -l info -f logs/info.log
