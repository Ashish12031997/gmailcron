from django_celery_beat.models import CrontabSchedule, PeriodicTask
import uuid
import logging
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)


def delete_emails():
    minute = '*'
    hour = '*'
    day = '*'
    month = '*'
    
    cron_job, created = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_month=str(day),
            month_of_year=str(month),
        )
    
    celery_task_name = str(uuid.uuid4())
    task_name = "cron_app.tasks.delete_emails"
    queue = "delete_emails"
    routing_key = "delete_emails"
    task = PeriodicTask.objects.create(crontab=cron_job,
            task=task_name,
            name=celery_task_name,
            queue=queue,
            routing_key=routing_key,
            # kwargs=json.dumps(basic_payload),
            one_off=False,)
    now = datetime.now()
    next_run_time = cron_job.human_readable
    # next_run_time = now + next_run_time
    print("Deleting email with id: ", next_run_time)
    logger.info("Scheduled delete_emails task to run every minute.")
    print("Scheduled delete_emails task to run every minute.")
    return "Email deleted"
