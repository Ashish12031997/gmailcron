from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cron_app.tasks import delete_emails


@api_view(["GET"])
def hello(request):
    delete_emails.apply_async(queue="delete_emails")
    return Response({"message": "Hello World"})
