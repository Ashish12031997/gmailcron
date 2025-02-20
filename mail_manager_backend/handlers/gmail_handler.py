from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from mail_manager_backend.services.gmail_services import GmailServices
from mail_manager_backend.models.token_model import TokenManager
from mail_manager_backend.models.user_model import Users
from mail_manager_backend.models.delete_emails_model import DeleteEmails
from mail_manager_backend.models.data_models.delete_email import (
    DeleteEmailList,
    DeleteEmail,
)


async def get_emailss():
    creds = Credentials.from_authorized_user_info(
        {
            "refresh_token": "1//04UX1vW1Clo9zCgYIARAAGAQSNwF-L9IrwQMCdcHlp10j8CcQheTYJGxZw47n0oDfl7Gg4ohFFPnG86WKpfpTiKQ5U1G2PxfTbEM",
            "client_id": "322672977807-3o8e8gvvd9tnrlgjrb93pfq205fafq7l.apps.googleusercontent.com",
            "client_secret": "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",
        }
    )

    service = GmailServices(creds)
    messages = await service.get_messages()
    return {"emails": messages}


async def generate_token():
    SCOPES = [
        "https://mail.google.com/",
        "https://www.googleapis.com/auth/gmail.readonly",
    ]
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    print("Token created", creds.to_json(), flush=True)
    user: Users = await Users.asave(email="asa", first_name="asa", last_name="asa")
    await TokenManager.save_token(
        user_id=user.id,
        token=creds.token,
        refresh_token=creds.refresh_token,
        token_uri=creds.token_uri,
        client_id=creds.client_id,
        client_secret=creds.client_secret,
        scopes=creds.scopes,
        expires_at=creds.expiry.timestamp(),
        universe_domain="gmail.com",
        account="",
    )
    return {"status": creds.to_json()}


async def add_emails_to_delete(user_id: int, emails: list[str]):
    emails_to_delete = DeleteEmailList(
        email=[DeleteEmail(email=email, user_id=user_id) for email in emails]
    )

    await DeleteEmails.objects.bulk_create(
        emails=emails_to_delete,
    )


async def remove_emails(user_id: int, emails: list[str]):
    DeleteEmails.objects.filter(email__in=emails, user_id=user_id).adelete()
    return {"status": "running"}


async def delete_emails_by_users(user_id: int):
    email_ids = await DeleteEmails.objects.filter(user_id=user_id)
    emails = [email.email for email in email_ids]
    user = await Users.objects.aget(id=user_id)

    token = await TokenManager.get_token_by_user_id(user_id=user.id)

    creds = Credentials.from_authorized_user_info(
        {
            "refresh_token": token.refresh_token,
            "client_id": token.client_id,
            "client_secret": token.client_secret,
        }
    )
    service = GmailServices(creds)
    emails = [email.email for email in email_ids]
    for email in emails:
        print(email, flush=True)

        messages = await service.get_messages(email)
        await service.delete_messages(messages)
        print("email ids", messages, flush=True)
    return {"status": "running"}
