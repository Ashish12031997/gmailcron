from celery import shared_task


@shared_task(bind=True)
def delete_emails():
    print("Deleting email with id: ")
    return "Email deleted"
