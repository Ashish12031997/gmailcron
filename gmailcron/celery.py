from __future__ import absolute_import, unicode_literals

import os
from urllib.parse import quote_plus

from celery import Celery
from django.conf import settings

# from main.secret_and_configuration.constant import (
#     RABBIT_MQ_ENDPOINT,
#     RABBIT_MQ_PASSWORD,
#     RABBIT_MQ_USER,
# )

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "gmailcron.settings"
)

app = Celery("gmailcron")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace="CELERY")
rabbit_mq_password = quote_plus("redis_password")
app.conf.update(
    {
        "broker_url": f"amqp://:redis_password@0.0.0.0",
        "task_serializer": "json",
        "task_acks_late": True,
        "result_serializer": "json",
        "result_backend": "django-db",
        "accept_content": ["json"],
        "backend": f"amqp://:redis_password@0.0.0.0",
        "worker_prefetch_multiplier": 1,
        "worker_cancel_long_running_tasks_on_connection_loss": True,
        "result_extended": True,
        "task_reject_on_worker_lost": True,
        "broker_connection_retry_on_startup": True,
    }
)
app.conf.beat_scheduler = (
    "gmailcron.celery_beat_scheduler:DatabaseScheduler"
)

#  Routing task to different queue
app.conf.task_routes = {
    "cron_app.tasks.delete_emails": {"queue": "delete_emails"}
}

# app.conf.task_routes = (
#     [
#         ("main.tasks.schedule_publish_photo", {"queue": "instagram_normal_post"}),
#         ("main.tasks.schedule_publish_video", {"queue": "instagram_video_post"}),
#         ("main.tasks.publish_carousel", {"queue": "instagram_video_post"}),
#     ],
# )


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
