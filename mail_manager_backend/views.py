from uuid import uuid4

from django.shortcuts import render
from django_celery_beat.models import CrontabSchedule, PeriodicTask, PeriodicTasks

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mail_manager_backend.tasks import delete_emails


@api_view(["GET"])
def hello(request):
    delete_emails.apply_async(queue="delete_emails")
    return Response({"message": "Hello World"})


@api_view(["GET"])
def get_tasks(request):
    new_task_id = str(uuid4())
    crontab, exits = CrontabSchedule.objects.get_or_create(
        minute="*/1",
    )
    task_info = dict(
        task="mail_manager_backend.tasks.delete_emails",
        crontab=crontab,
        queue="delete_emails",
        one_off=False,  # if you want to disable task atfer first run make it true default is False
        enabled=True,  # if you ouly want to create task but don't want to run it make it false default is True
    )
    task_created, is_updated = PeriodicTask.objects.update_or_create(
        name=new_task_id,
        defaults=task_info,
    )
    PeriodicTasks.update_changed()
    return Response({"message": "Task Created"})
