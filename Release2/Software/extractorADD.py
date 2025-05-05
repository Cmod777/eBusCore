#!/usr/bin/env python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys

# === CONFIGURATION ===
CREDS_PATH = 'path/to/credentials.json'
SPREADSHEET_NAME = 'Your Spreadsheet Name'
SOURCE_SHEET_NAME = 'SourceSheet'
LEGEND_SHEET_NAME = 'LegendSheet'
TARGET_SHEET_NAME = 'ProcessedSheet'
LOG_PATH = 'data_extraction.log'

# === LOGGING ===
class Logger:
    def __init__(self, logfile):
        self.terminal = sys.stdout
        self.log = open(logfile, "a", encoding="utf-8")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger(LOG_PATH)
print(f"\n\n[{datetime.now().isoformat()}] === START ===")

# === AUTHENTICATION ===
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
client = gspread.authorize(creds)

# === LOAD SHEETS ===
spreadsheet = client.open(SPREADSHEET_NAME)
source_sheet = spreadsheet.worksheet(SOURCE_SHEET_NAME)
legend_sheet = spreadsheet.worksheet(LEGEND_SHEET_NAME)
target_sheet = spreadsheet.worksheet(TARGET_SHEET_NAME)

# === READ DATA ===
source_data = source_sheet.get_all_values()
source_headers = [h.strip() for h in source_data[0]]
source_rows = source_data[4:]
legend_data = legend_sheet.get_all_values()

# === BUILD COLUMN MAP BASED ON LEGEND ===
column_map = {}
for row in legend_data:
    if len(row) >= 6:
        name = row[0].strip()
        code_col = row[2].strip()
        code_arg = row[3].strip()
        code_area = row[4].strip()
        include = row[5].strip().upper()
        if include == "YES" and code_col:
            column_map[name] = {
                "code": code_col,
                "arg": code_arg,
                "area": code_area
            }

# === IDENTIFY INCLUDED COLUMNS ===
headers, args, areas, indices = [], [], [], []
timestamp_index = None

for i, name in enumerate(source_headers):
    if name == "timestamp":
        timestamp_index = i
    if name in column_map:
        info = column_map[name]
        headers.append(info["code"])
        args.append(info["arg"])
        areas.append(info["area"])
        indices.append(i)

print(f"Included {len(headers)} columns: {headers}")
if timestamp_index is None:
    print("ERROR: 'timestamp' column not found!")
    sys.exit(1)

# === NORMALIZATION FUNCTION ===
def normalize(val):
    val = str(val).strip()
    return val.replace(",", ".") if val else "NaN"

# === FIND LAST TIMESTAMP IN TARGET SHEET ===
target_data = target_sheet.get_all_values()
last_timestamp = None
if len(target_data) > 3:
    last_row = target_data[-1]
    if len(last_row) > 0:
        last_timestamp = last_row[0].strip()

print(f"Last timestamp found in target sheet: {last_timestamp}")

# === FILTER NEW ROWS ===
new_rows = []
for row in source_rows:
    if timestamp_index >= len(row):
        continue
    ts = row[timestamp_index].strip()
    if not ts:
        continue
    if last_timestamp is None or ts > last_timestamp:
        filtered = [normalize(row[i]) if i < len(row) else "NaN" for i in indices]
        new_rows.append(filtered)

print(f"New rows found to add: {len(new_rows)}")

# === WRITE HEADERS AND METADATA ===
target_sheet.update(range_name="A1", values=[headers])
target_sheet.update(range_name="A2", values=[args])
target_sheet.update(range_name="A3", values=[areas])

# === WRITE NEW DATA ROWS ===
if new_rows:
    start_row = len(target_data) + 1
    target_sheet.update(range_name=f"A{start_row}", values=new_rows)
    print(f"SUCCESS: Added {len(new_rows)} new rows starting at row {start_row}.")
    print("Preview of first new row:")
    print(new_rows[0] if new_rows else "[Empty]")
else:
    print("INFO: No new rows to write.")

print(f"[{datetime.now().isoformat()}] === END ===")
