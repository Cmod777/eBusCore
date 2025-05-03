#!/usr/bin/env python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Config ===
CREDS_PATH = 'ADD_YOUR_JSON_CREDENTIALS_PATH.json'
SPREADSHEET_NAME = 'ADD_YOUR_SPREADSHEET_NAME'
SOURCE_SHEET_NAME = 'PAGE_NAME_SOURCE'
LEGEND_SHEET_NAME = 'PAGE_NAME_LEGEND'
TARGET_SHEET_NAME = 'PAGE_NAME_TARGET'

# === Auth ===
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
client = gspread.authorize(creds)

# === Load sheets ===
spreadsheet = client.open(SPREADSHEET_NAME)
source = spreadsheet.worksheet(SOURCE_SHEET_NAME)
legend = spreadsheet.worksheet(LEGEND_SHEET_NAME)
target = spreadsheet.worksheet(TARGET_SHEET_NAME)

# === Read data ===
source_data = source.get_all_values()
legend_data = legend.get_all_values()
source_headers = source_data[0]
source_rows = source_data[1:]

# === Build legend map ===
legend_map = {}
for row in legend_data:
    if len(row) >= 3 and row[2].strip().isdigit():
        label = row[0].strip()
        code = row[2].strip()
        legend_map[label] = code

# === Define excluded columns ===
excluded_codes = {'101', '114', '119', '125', '129', '142', '146', '148', '151', '163', '170', '176'}

# === Filter headers ===
final_headers = []
col_indices = []
for i, name in enumerate(source_headers):
    code = legend_map.get(name.strip())
    if code and code not in excluded_codes and not code.startswith('NO'):
        final_headers.append(code)
        col_indices.append(i)

# === Build clean data ===
clean_rows = []
for row in source_rows:
    clean = [row[i] if i < len(row) and row[i] else 'NaN' for i in col_indices]
    clean_rows.append(clean)

# === Read existing data from target ===
existing_data = target.get_all_values()
existing_count = len(existing_data) - 1  # exclude header

# === Select only new rows ===
new_rows = clean_rows[existing_count:] if existing_count < len(clean_rows) else []

# === Expand sheet if needed ===
required_rows = existing_count + len(new_rows) + 1
if required_rows > target.row_count:
    target.add_rows(required_rows - target.row_count)

# === Append new rows ===
if new_rows:
    start_cell = f"A{existing_count + 2}"
    target.update(values=new_rows, range_name=start_cell)
    print(f"Done. Appended {len(new_rows)} new rows to '{TARGET_SHEET_NAME}'.")
else:
    print("No new rows to write.")
