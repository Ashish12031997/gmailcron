from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from mail_manager_backend.handlers.delete_emails_job import delete_emails


@api_view(["GET"])
def health_check(request):
    return Response({"status": "healthy"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def update_delete_emails(request):
    delete_emails()
    return Response({"status": "healthy"}, status=status.HTTP_200_OK)
