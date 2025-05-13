#!/usr/bin/env python3
# Script: download_data.py
# Purpose: Downloads the sheet named "Data" from Google Sheets and saves it locally as "data.csv",
#          correctly escaping newline characters within cells.

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# === CONFIGURATION ===
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'  # Replace with your Google Sheets ID
TAB_NAME = 'Data'
OUTPUT_FILE = 'data.csv'

# === AUTHENTICATION ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope) # Ensure your credentials file is named 'credentials.json'
client = gspread.authorize(creds)

# === ACCESSING THE SHEET ===
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(TAB_NAME)
all_rows = sheet.get_all_values()

# === WRITING TO CSV FILE (CORRECT NEWLINE ESCAPING) ===
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    for row in all_rows:
        writer.writerow([cell.replace('\n', '\\n') for cell in row])

print("[OK] Sheet 'Data' saved successfully as 'data.csv'")
