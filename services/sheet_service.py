import os
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
creds_file_path = os.path.join(parent_dir, 'sheets-key.json')

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file_path, scope)

client = gspread.authorize(credentials)

sheet = client.open('Заявки на Путь роста')
time.sleep(1)
sheet.share('email@gmail.com', perm_type='user', role='writer')
