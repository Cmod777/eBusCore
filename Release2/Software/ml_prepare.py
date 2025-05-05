#!/usr/bin/env python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys

# === CONFIGURATION ===
CREDS_PATH = 'path/to/your/credentials.json'  # Replace with the path to your credentials file
SPREADSHEET_NAME = 'Your Spreadsheet Name'
SOURCE_SHEET_NAME = 'RawData'
TARGET_SHEET_NAME = 'CleanData'
LOG_PATH = 'prepare_data.log'

# === ALLOWED COLUMNS (example codes, replace with real ones as needed) ===
ALLOWED_CODES = {
    'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08',
    'A09', 'A10', 'B01', 'B02', 'B03', 'B04', 'B05', 'C01',
    'C02', 'C03', 'D01', 'D02', 'D03', 'D04', 'E01', 'E02',
    'F01', 'F02', 'F03', 'G01', 'G02', 'H01', 'H02', 'I01'
}

SPECIAL_NAN_CODES = {'E01', 'E02'}
BINARY_CODES = {'A02', 'D01'}
DISCRETE_CODES = {'F01', 'F02'}
NO_INTERPOLATION = {'C03', 'G01'}

# === LOGGING CLASS ===
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
source = spreadsheet.worksheet(SOURCE_SHEET_NAME)
try:
    target = spreadsheet.worksheet(TARGET_SHEET_NAME)
except gspread.exceptions.WorksheetNotFound:
    target = spreadsheet.add_worksheet(title=TARGET_SHEET_NAME, rows="10", cols="10")
    print(f"Created new sheet '{TARGET_SHEET_NAME}' as it did not exist.")

# === READ DATA ===
data = source.get_all_values()
headers = data[0]
meta1 = data[1]
meta2 = data[2]
rows = data[3:]

# === FILTER ALLOWED COLUMNS ===
col_map = [(i, headers[i]) for i in range(len(headers)) if headers[i] in ALLOWED_CODES]
if not col_map:
    print("ERROR: No allowed columns found.")
    sys.exit(1)

filtered_indices = [i for i, _ in col_map]
filtered_codes = [code for _, code in col_map]
print(f"Included {len(filtered_codes)} columns: {filtered_codes}")

# === FIND TIMESTAMP INDEX (assuming 'A01' is timestamp) ===
try:
    timestamp_index = headers.index("A01")
except ValueError:
    print("ERROR: Timestamp column 'A01' not found.")
    sys.exit(1)

# === GET LAST TIMESTAMP IN TARGET SHEET ===
target_data = target.get_all_values()
last_timestamp = None
if len(target_data) > 3:
    last_row = target_data[-1]
    if len(last_row) > 0:
        last_timestamp = last_row[0].strip()
print(f"Last timestamp in target sheet: {last_timestamp}")

# === -999 CHECK FUNCTION ===
def is_invalid_999(value):
    norm = value.strip().replace(',', '.')
    try:
        return float(norm) == -999.0
    except:
        return False

# === FILTER ROWS ===
new_rows = []
count_written = 0

for row in rows:
    if timestamp_index >= len(row):
        continue
    ts = row[timestamp_index].strip()
    if not ts:
        continue
    if last_timestamp and ts <= last_timestamp:
        continue
    new_row = []
    for i, code in zip(filtered_indices, filtered_codes):
        val = row[i].strip().replace(',', '.') if i < len(row) else ""
        if code in NO_INTERPOLATION:
            new_row.append("NaN")
        elif is_invalid_999(val):
            new_row.append("NaN")
        else:
            new_row.append(val or "NaN")
    new_rows.append(new_row)
    count_written += 1

# === BUILD FINAL OUTPUT STRUCTURE ===
row1 = [code for code in filtered_codes]
row2 = [meta1[i] for i, _ in col_map]
row3 = [meta2[i] for i, _ in col_map]
final_data = [row1, row2, row3] + new_rows

# === WRITE TO TARGET SHEET ===
target.update(values=final_data, range_name='A1')
print(f"SUCCESS: {count_written} new rows written.")
if new_rows:
    print("Preview of first new row:")
    print(new_rows[0])
else:
    print("No new rows to write.")

print(f"[{datetime.now().isoformat()}] === END ===")
