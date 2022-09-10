from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
with open('token.json', 'rb') as token:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

service = build('gmail', 'v1', credentials=creds)
profile = service.users().getProfile(userId='me').execute()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
with open('token.json', 'rb') as token:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

service = build('gmail', 'v1', credentials=creds)

filter = service.users().messages().list(userId = 'me', maxResults=10,
                                         q = 'from:no_reply@accessbankplc.com \
                                             subject:AccessAlert Transaction Alert').execute()

filter_id = filter['messages']
id_lst = []
for ids in filter_id:
    id_lst.append(ids['id'])
    
trans_lst = []
for each_id in id_lst:
    msgs = service.users().messages().get(userId = 'me', id = each_id).execute()
    snippet = msgs['snippet']
    main_body = msgs['payload']['body']['data']
    main_body = main_body.replace('-', '+').replace('_', '/')
    decode_msg = base64.b64decode(main_body)
    soup = bs(decode_msg, 'lxml')
    details = soup.find_all('tr')[7]
    
    description = details.find_all('td')[6].text.replace('\r',' ').replace("\n"," ").strip()
    reference_number = details.find_all('td')[8].text.replace('\r',' ').replace("\n"," ").strip()
    trans_branch = details.find_all('td')[10].text.replace('\r',' ').replace("\n"," ").strip()
    date = msgs['payload']['headers'][-1]['value']
    amount = re.search('\d*\.+\d+', snippet).group()
    acct_no = re.search('\d*\*+\d+', snippet).group()
    
    if 'Credited' in snippet:
        trans_type = 'Credited'
    else:
        trans_type = 'Debited'
    
    
    trans_lst.append({
        'amount': amount,
        'a/c_number': acct_no,
        'trans_type': trans_type,
        'description': description,
        'reference_number': reference_number,
        'trans_branch': trans_branch,
        'datetime': date
    })
cols_name = ['amount', 'a/c_number', 'trans_type', 'description', 'reference_number', 'trans_branch', 'datetime']
data = pd.DataFrame(trans_lst, columns=cols_name)

print(profile)
print(data)