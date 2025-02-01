
from django.urls import path
from cron_app.handlers.health_check import health_check, update_delete_emails
from cron_app.handlers.delete_emails_job import delete_emails
app_name = "cron"

urlpatterns = [
    path("health-check/", health_check, name="health-check"),
    path("update-delete-emails/", update_delete_emails, name="update-delete-emails"),
]


