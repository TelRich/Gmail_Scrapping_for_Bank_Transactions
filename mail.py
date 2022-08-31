from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
with open('token.json', 'rb') as token:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

service = build('gmail', 'v1', credentials=creds)
result = service.users().messages().list(userId='me').execute()
messages = result.get('messages')
messages
