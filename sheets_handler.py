from datetime import datetime

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

from custom_exceptions import (
    NoCurrentWorkSheet, MoreThanTwoCurrentWorkSheets, GetWorksheetError, NoSpreadsheetFound
)
from src.common.settings import Settings


class GoogleSheetsAPI:
    def __init__(
            self,
            creds_file: str = Settings.GOOGLE_CREDENTIALS,
            spreadsheet_id: str = Settings.SPREADSHEET_ID,
    ):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        self.client = gspread.authorize(creds)
        self.spreadsheet_id = spreadsheet_id

    def get_as_dataframe(self):
        try:
            sheet = self.client.open_by_key(self.spreadsheet_id)
        except Exception as e:
            raise NoSpreadsheetFound(self.spreadsheet_id, e)
        current_worksheet = [ws for ws in sheet.worksheets() if Settings.CURRENT_WORKSHEET_PREFIX in ws.title]
        if not current_worksheet:
            raise NoCurrentWorkSheet(self.spreadsheet_id)
        elif len(current_worksheet) > 1:
            raise MoreThanTwoCurrentWorkSheets(self.spreadsheet_id)
        try:
            return get_as_dataframe(current_worksheet[0])
        except Exception as e:
            raise GetWorksheetError(self.spreadsheet_id, current_worksheet[0].title, e)

    def set_with_dataframe(self, df):
        try:
            sheet = self.client.open_by_key(self.spreadsheet_id)
        except Exception as e:
            raise NoSpreadsheetFound(self.spreadsheet_id, e)

        # If there's already a 'current' worksheet, rename it to its date only
        current_worksheets = [ws for ws in sheet.worksheets() if Settings.CURRENT_WORKSHEET_PREFIX in ws.title]
        if current_worksheets:
            for ws in current_worksheets:
                new_title = ws.title.strip(Settings.CURRENT_WORKSHEET_PREFIX)
                ws.update_title(new_title)

        date_string = datetime.now().strftime('%d-%m-%Y')
        worksheet_name = f'current_{date_string}'
        worksheet = sheet.add_worksheet(title=worksheet_name, rows="1", cols="1")
        set_with_dataframe(worksheet, df)
        sheet.reorder_worksheets([worksheet.id] + [ws.id for ws in sheet.worksheets() if ws.id != worksheet.id])

