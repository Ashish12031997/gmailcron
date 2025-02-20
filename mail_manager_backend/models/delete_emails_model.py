from django.db import models

class DeleteEmails(models.Model):
    email = models.EmailField(max_length=255, null=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        db_table = "delete_emails"
