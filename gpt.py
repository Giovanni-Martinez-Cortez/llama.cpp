from flask import Flask
import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Path to your credentials JSON file
CREDENTIALS_FILE = "credentials.json"
# Google Sheets ID (Get this from the URL of your Google Sheet)
SPREADSHEET_ID = "1ndk3EjqFxQxZMAFokVS5hhqhAXNwAp6DgdRUwsFV8I8"

# Flask app setup
app = Flask(__name__)

# Google Sheets API setup
def append_to_google_sheet(data):
    # Authenticate using the credentials file
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build('sheets', 'v4', credentials=creds)

    # Append data to the Google Sheet
    sheet = service.spreadsheets()
    body = {"values": [data]}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A:C",  # Adjust range if needed
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

    return result

@app.route('/test')
def test_google_sheets():
    # Test data to log
    test_data = [
        "test_qr_code",
        "Test Exhibit",
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]

    # Append test data to Google Sheet
    result = append_to_google_sheet(test_data)

    return f"Data appended to Google Sheets! {result}"

if __name__ == "__main__":
    app.run(debug=True)
