import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
creds_file_path = os.path.join(parent_dir, 'google_creds.json')

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file_path, scope)

client = gspread.authorize(credentials)

# sheet = client.create('Заявки на крещение')
# sheet.share('moisey.kirillov@gmail.com', perm_type='user', role='writer')
