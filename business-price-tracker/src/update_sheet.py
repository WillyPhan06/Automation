import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from utils import log_info, log_error

# Define the scope
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Load credentials
def connect_to_sheets(creds_file, sheet_name):
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        log_info(f"Connected to Google Sheet: {sheet_name}")
        return sheet
    except Exception as e:
        log_error(f"Failed to connect to Google Sheet: {e}")
        return None

def read_cleaned_csv(csv_path):
    df = pd.read_csv(csv_path)
    log_info(f"Loaded {len(df)} rows from {csv_path}")
    return df

def update_sheet(sheet, df):
    try:
        sheet.clear()  # optional: remove old data

        # Insert headers
        sheet.insert_row(list(df.columns), index=1)

        # Insert rows
        for i, row in enumerate(df.values.tolist(), start=2):
            sheet.insert_row(row, index=i)

        log_info("Google Sheet updated successfully")
    except Exception as e:
        log_error(f"Failed to update sheet: {e}")

if __name__ == "__main__":
    creds_file = "credentials.json"
    sheet_name = "Business Tracker Sheet"

    sheet = connect_to_sheets(creds_file, sheet_name)
    if sheet:
        df = read_cleaned_csv("data/cleaned/cleaned_prices.csv")
        update_sheet(sheet, df)
