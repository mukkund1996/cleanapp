import gspread
import pandas as pd
from urllib3.exceptions import HTTPError
from retry import retry
from oauth2client.service_account import ServiceAccountCredentials
from cleanapp.config import CLEANING_MASTER_SHEET, CREDENTIALS_PATH


@retry(HTTPError, tries=3, delay=2)
def get_sheet(sheet_name=CLEANING_MASTER_SHEET, credentials=CREDENTIALS_PATH):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open(sheet_name)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    records = sheet_instance.get_all_records()

    records_df = pd.DataFrame.from_dict(records).set_index('week_no')

    return sheet_instance, records_df
