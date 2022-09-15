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

def extract_transaction(maxResult=50, excel = False, csv=False):
    # Filtering for transaction mails
    filter = service.users().messages().list(userId = 'me', maxResults=maxResult,
                                         q = 'from:no_reply@accessbankplc.com \
                                             subject:AccessAlert Transaction Alert').execute()

    # Extracting Ids from filtered mail
    filter_id = filter['messages']
    id_lst = []
    for ids in filter_id:
        id_lst.append(ids['id'])
    
    # Accessing trasaction summary
    trans_lst = []
    for each_id in id_lst:
        msgs = service.users().messages().get(userId = 'me', id = each_id).execute()
        snippet = msgs['snippet']
        main_body = msgs['payload']['body']['data']
        main_body = main_body.replace('-', '+').replace('_', '/')
        decode_msg = base64.b64decode(main_body)
        soup = bs(decode_msg, 'lxml')
        details = soup.find_all('tr')[7]
        
        # Extracting required parameters from transaction summary
        description = details.find_all('td')[6].text.replace('\r',' ').replace("\n"," ").strip()
        reference_number = details.find_all('td')[8].text.replace('\r',' ').replace("\n"," ").strip()
        trans_branch = details.find_all('td')[10].text.replace('\r',' ').replace("\n"," ").strip()
        date = msgs['payload']['headers'][-1]['value']
        amount = re.search('\d*\.+\d+', snippet).group()
        acct_no = re.search('\d*\*+\d+', snippet).group()
        
        # Checking the type of transaction
        if 'Credited' in snippet:
            trans_type = 'Credited'
        else:
            trans_type = 'Debited'
        
        # Appending extracted parameters to a dictionary
        trans_lst.append({
            'amount': float(amount),
            'a/c_number': acct_no,
            'trans_type': trans_type,
            'description': description,
            'reference_number': reference_number,
            'trans_branch': trans_branch,
            'datetime': pd.to_datetime(date).tz_localize(None)
        })


    # Assigning columns names and returning a dataframe of extracted parameters
    cols_name = ['amount', 'a/c_number', 'trans_type', 'description', 'reference_number', 'trans_branch', 'datetime']
    data = pd.DataFrame(trans_lst, columns=cols_name)
    
    if excel:
        data.to_excel("transaction.xlsx")
    elif csv:
        data.to_csv("transaction.csv", index=False)
        
    print(data)

if __name__ == '__main__':
    extract_transaction(5)
