import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/", "https://www.googleapis.com/auth/gmail.readonly"]


class GmailServices:

    def __init__(self, creds):
        self.service = build("gmail", "v1", credentials=creds)

    async def get_messages(self, email):
        results = (
            self.service.users()
            .messages()
            .list(userId="me", q=f"from:{email}")
            .execute()
        )
        email_ids = []
        if results["resultSizeEstimate"] > 0:
            email_ids = [n.get("id") for n in results["messages"]]

        return email_ids

    async def delete_messages(self, email_ids: list) -> None:

        self.service.users().messages().batchDelete(
            userId="me", body={"ids": email_ids}
        ).execute()

    def main(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            # creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            creds = Credentials.from_authorized_user_info(
                {
                    "refresh_token": "1//04UX1vW1Clo9zCgYIARAAGAQSNwF-L9IrwQMCdcHlp10j8CcQheTYJGxZw47n0oDfl7Gg4ohFFPnG86WKpfpTiKQ5U1G2PxfTbEM",
                    "client_id": "322672977807-3o8e8gvvd9tnrlgjrb93pfq205fafq7l.apps.googleusercontent.com",
                    "client_secret": "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",
                }
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
