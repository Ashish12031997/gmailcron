from django.urls import path
from mail_manager_backend.handlers.health_check import (
    health_check,
    update_delete_emails,
)
from mail_manager_backend.handlers.delete_emails_job import delete_emails

app_name = "gmail"

urlpatterns = [
    path("health-check/", health_check, name="health-check"),
    path("update-delete-emails/", update_delete_emails, name="update-delete-emails"),
]
