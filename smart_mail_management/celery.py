from __future__ import absolute_import, unicode_literals

import os
from urllib.parse import quote_plus

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_mail_management.settings")

app = Celery("smart_mail_management")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace="CELERY")
rabbit_mq_password = quote_plus("redis_password")

# get below creds from env
app.conf.update(
    {
        "broker_url": f"redis://redis:6379",
        "task_serializer": "json",
        "task_acks_late": True,
        "result_serializer": "json",
        "result_backend": "django-db",
        "accept_content": ["json"],
        "backend": f"redis://redis:6379",
        "worker_prefetch_multiplier": 1,
        "worker_cancel_long_running_tasks_on_connection_loss": True,
        "result_extended": True,
        "task_reject_on_worker_lost": True,
        "broker_connection_retry_on_startup": True,
    }
)
app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

#  Routing task to different queue
app.conf.task_routes = {
    "mail_manager_backend.tasks.delete_emails": {"queue": "delete_emails"}
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
