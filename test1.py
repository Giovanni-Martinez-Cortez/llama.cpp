from flask import Flask, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

app = Flask(__name__)

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"  # Replace with the path to your credentials file
SPREADSHEET_NAME = "Scan Data Log"  # Replace with the name of your Google Sheet

# Authorize and open the sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
gc = gspread.authorize(credentials)
sheet = gc.open(SPREADSHEET_NAME).sheet1

@app.route('/')
def index():
    return 'Welcome to the QR Code Scan App! Please scan a QR code by appending it to the URL like /scan/<qr_code_id>.'

@app.route('/scan/<qr_code_id>')
def scan(qr_code_id):
    # Map QR code IDs to exhibit names
    exhibit_mapping = {
        "fish001": "Fish Exhibit",
        "monkey001": "Monkey Exhibit",
    }
    exhibit_name = exhibit_mapping.get(qr_code_id, "Unknown Exhibit")
    
    # Log the scan
    log_scan(qr_code_id, exhibit_name)
    
    # Redirect to the appropriate page
    if exhibit_name != "Unknown Exhibit":
        return redirect(f"https://gioinfocus.com/exhibit/{qr_code_id}")
    else:
        return f"Exhibit not found for QR Code: {qr_code_id}", 404

def log_scan(qr_code_id, exhibit_name):
    # Log data to Google Sheets
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([qr_code_id, exhibit_name, timestamp])
    except Exception as e:
        print(f"Error appending data to Google Sheets: {e}")

if __name__ == "__main__":
    # Use the environment's PORT variable or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
