import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from models.meeting_request import MeetingRequest

current_dir = os.getcwd()
creds_file_path = os.path.join(current_dir, 'sheets-key.json')

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file_path, scope)


def add_new_site_request(request: MeetingRequest):
    client = gspread.authorize(credentials)
    spreadsheet = client.open('Заявки на Путь роста')
    worksheet_title = f'{request.step_number} шаг'
    worksheet = spreadsheet.worksheet(worksheet_title)
    values = worksheet.get_all_values()
    first_empty_row = len(values) + 1
    worksheet.update_cell(first_empty_row, 1, request.meeting_title)
    worksheet.update_cell(first_empty_row, 2, request.date)
    worksheet.update_cell(first_empty_row, 3, request.first_name)
    worksheet.update_cell(first_empty_row, 4, request.last_name)
    worksheet.update_cell(first_empty_row, 5, request.telegram_login)


def mark_visit_is_completed(request: MeetingRequest):
    client = gspread.authorize(credentials)
    spreadsheet = client.open('Заявки на Путь роста')
    worksheet_title = f'{request.step_number} шаг'
    mark_cell_number = 6 if request.meeting_number == 1 else 7 \
        if request.meeting_number == 2 else 8 \
        if request.meeting_number == 3 else 9
    worksheet = spreadsheet.worksheet(worksheet_title)
    values = worksheet.get_all_values()
    for index, row in enumerate(values):
        if row[1] == request.date \
                and row[2] == request.first_name \
                and row[3] == request.last_name \
                and row[4] == request.telegram_login:
            worksheet.update_cell(index + 1, mark_cell_number, 'Пришел')
