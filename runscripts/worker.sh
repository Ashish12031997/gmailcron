#!/usr/bin/env bash
celery -A gmailcron  worker -c "4" -Q delete_emails -l info -f logs/info.log -n gmail_delete_emails.%h --without-gossip --without-mingle  --without-heartbeat -Ofair
