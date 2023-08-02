

class NoSpreadsheetFound(Exception):
    def __init__(self, spreadsheet_id, error):
        self.message = f"Spreadsheet with ID: {spreadsheet_id} is not found. Error: {error}"


class NoCurrentWorkSheet(Exception):
    def __init__(self, spreadsheet_id):
        self.message = f"Current worksheet is not found in the spreadsheet with ID: {spreadsheet_id}"


class MoreThanTwoCurrentWorkSheets(Exception):
    def __init__(self, spreadsheet_id):
        self.message = f"There are more than two current worksheets in the spreadsheet with ID: {spreadsheet_id}. Please refresh it."


class GetWorksheetError(Exception):
    def __init__(self, spreadsheet_id, sheet_name, error):
        self.message = f"Cannot get worksheet {sheet_name} from the spreadsheet with ID: {spreadsheet_id}. Error: {error}."
