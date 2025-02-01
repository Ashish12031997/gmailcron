from celery import shared_task


@shared_task(bind=True)
def delete_emails(self,):
    print("Deleting email with id: ")
    return "Email deleted"
