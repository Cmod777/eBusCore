#!/usr/bin/env python3
# Script: importDB.py
# Purpose: Downloads the "Data" sheet from Google Sheets and saves it locally as "db.csv",
#          correctly escaping newline characters within cells

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# === CONFIGURATION ===
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'  # Replace with your Google Sheets ID
TAB_NAME = 'Data'
OUTPUT_FILE = 'db.csv'
CREDENTIALS_FILE = 'your_credentials.json' # Replace with your credentials file name

# === AUTHENTICATION ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# === ACCESSING THE SHEET ===
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(TAB_NAME)
all_rows = sheet.get_all_values()

# === WRITING TO CSV FILE (CORRECT ESCAPING OF NEWLINES) ===
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    for row in all_rows:
        writer.writerow([cell.replace('\n', '\\n') for cell in row])

print("[OK] Sheet 'Data' successfully saved as 'db.csv'")
