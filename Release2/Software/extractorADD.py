#!/usr/bin/env python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys

# === CONFIGURATION ===
CREDS_PATH = 'path/to/your/creds.json'  # Replace with your credentials path
SPREADSHEET_NAME = 'Your Spreadsheet Name'
RAW_SHEET_NAME = 'raw_data'
METADATA_SHEET_NAME = 'metadata'
OUTPUT_SHEET_NAME = 'output_data'
LOG_PATH = 'extractor.log'

# === SETUP LOGGING ===
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
raw = spreadsheet.worksheet(RAW_SHEET_NAME)
meta = spreadsheet.worksheet(METADATA_SHEET_NAME)
output = spreadsheet.worksheet(OUTPUT_SHEET_NAME)

# === READ DATA ===
raw_data = raw.get_all_values()
legend_data = meta.get_all_values()

raw_headers = raw_data[0]         # Row 1: column names
raw_rows = raw_data[4:]           # From row 5: actual data

# === BUILD METADATA MAP (only included columns) ===
column_map = {}
for row in legend_data:
    if len(row) >= 6:
        name = row[0].strip()
        code = row[2].strip()
        subtitle1 = row[3].strip()
        subtitle2 = row[4].strip()
        include = row[5].strip().upper()
        if include == "YES" and code:
            column_map[name] = {
                "code": code,
                "subtitle1": subtitle1,
                "subtitle2": subtitle2
            }

# === EXTRACT STRUCTURE ===
headers = []
sub1 = []
sub2 = []
indices = []

for i, name in enumerate(raw_headers):
    if name.strip() in column_map:
        entry = column_map[name.strip()]
        headers.append(entry["code"])
        sub1.append(entry["subtitle1"])
        sub2.append(entry["subtitle2"])
        indices.append(i)

print(f"Including {len(headers)} columns:")
for h, s1, s2 in zip(headers, sub1, sub2):
    print(f"  - {h}: {s1} / {s2}")

# === EXTRACT ROWS ===
data_rows = []
for row in raw_rows:
    filtered = [row[i] if i < len(row) and row[i] else "NaN" for i in indices]
    data_rows.append(filtered)

print(f"Preparing to write {len(data_rows)} data rows.")

# === EXPAND SHEET IF NEEDED ===
total_rows = len(data_rows) + 3
total_cols = len(headers)

if total_rows > output.row_count:
    output.add_rows(total_rows - output.row_count)
if total_cols > output.col_count:
    output.add_cols(total_cols - output.col_count)

# === WRITE TO OUTPUT SHEET ===
output.update(range_name="A1", values=[headers])
output.update(range_name="A2", values=[sub1])
output.update(range_name="A3", values=[sub2])

if data_rows:
    output.update(range_name="A4", values=data_rows)
    print(f"SUCCESS: Wrote {len(data_rows)} rows to '{OUTPUT_SHEET_NAME}'.")
else:
    print("WARNING: No data rows to write.")

print(f"[{datetime.now().isoformat()}] === END ===")
