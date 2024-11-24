import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"  # Replace with the path to your credentials file
SPREADSHEET_NAME = "Scan Data Log"  # Replace with the name of your Google Sheet

# Authorize and open the sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
gc = gspread.authorize(credentials)
sheet = gc.open(SPREADSHEET_NAME).sheet1

def manual_test():
    # Manual test data to be added to the Google Sheet
    test_data = ["test_code", "test_exhibit", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    
    try:
        # Append the test row
        sheet.append_row(test_data)
        print("Test row added successfully!")
    except Exception as e:
        print(f"Error adding test row: {e}")

if __name__ == "__main__":
    manual_test()
