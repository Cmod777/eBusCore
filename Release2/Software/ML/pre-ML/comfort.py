#!/usr/bin/env python3

import sys
import os
from datetime import datetime
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# CONFIGURATION
# Adjust the following variables or set via environment variables
BASE_DIR          = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH  = os.getenv('GS_CREDS', os.path.join(BASE_DIR, 'credentials.json'))
SHEET_NAME        = os.getenv('GS_SHEET_NAME', 'YOUR_SHEET_NAME')
WORKSHEET_NAME    = os.getenv('GS_WORKSHEET_NAME', 'YOUR_WORKSHEET_NAME')
LOG_FILE          = os.path.join(BASE_DIR, 'comfort_analysis.log')

# LOGGER SETUP
class Logger:
    def __init__(self, logfile):
        self.stdout = sys.stdout
        self.file = open(logfile, 'a', encoding='utf-8')
    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)
    def flush(self):
        self.stdout.flush()
        self.file.flush()

sys.stdout = Logger(LOG_FILE)
print(f"\n\n[{datetime.now().isoformat()}] === COMFORT ANALYSIS START ===")

# AUTHENTICATE WITH GOOGLE SHEETS API
print("[INFO] Authenticating with Google Sheets API...")
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPES)
client = gspread.authorize(creds)

# LOAD DATA FROM SHEET
print("[INFO] Loading data from sheet...")
sheet = client.open(SHEET_NAME)
worksheet = sheet.worksheet(WORKSHEET_NAME)
rows = worksheet.get_all_values()
if len(rows) < 4:
    print("[ERROR] Not enough rows: check sheet structure.")
    sys.exit(1)

# EXTRACT HEADER AND DATA
header = rows[0]
data_rows = rows[3:]
df = pd.DataFrame(data_rows, columns=header)
print(f"[INFO] Loaded {len(data_rows)} raw rows.")

# CONVERT COLUMNS TO NUMERIC
print("[INFO] Converting columns to numeric...")
df = df.apply(pd.to_numeric, errors='coerce')
print(f"[INFO] Numeric conversion complete: {len(df)} valid rows.")

# FILTER OUT UNKNOWN SEASON CODES
invalid = df['164'] == 0
if invalid.sum():
    print(f"[WARNING] Excluding {invalid.sum()} rows with season code=0.")
df = df[df['164'] != 0]
print(f"[INFO] Rows for analysis: {len(df)}.")

# DEFINE ROOM COLUMNS
ROOM_COLUMNS = {
    'living':  {'num':'145','flag':'120'},
    'bedroom': {'num':'147','flag':'126'},
    'bath':    {'num':'149','flag':None}
}
df['boiler_flag'] = df['143']

# CREATE DISCOMFORT FLAGS
for room, cols in ROOM_COLUMNS.items():
    df[f'{room}_discomfort'] = df[cols['num']] >= 3

# CONTINUOUS VARIABLES FOR CORRELATION
CONT_VARS = ['103','104','105','109','110','113','114']
print("[INFO] Continuous variable correlation matrix:")
print(df[CONT_VARS].corr())

# MAPPING FUNCTIONS
def map_numeric_to_label(val):
    labels = {0:'Normal',1:'Very Comfortable',2:'Slightly Comfortable',
              3:'Moderate Discomfort',4:'High Discomfort',5:'Extreme',
              6:'Dry Cold',7:'Humid Cold',8:'Dry Heat',9:'Humid Heat'}
    try:
        return labels[int(val)]
    except:
        return 'Unknown'

# ROOM ANALYSIS FUNCTION
def analyze_room(name, cols):
    print(f"\n=== ANALYSIS: {name.upper()} ===")
    temp_col = cols['num']
    flag_col = cols['flag']
    df_room = df.copy()

    # DISTRIBUTION OF COMFORT LABELS
    df_room['label'] = df_room[temp_col].apply(map_numeric_to_label)
    dist = df_room.groupby(['164','label']).size().unstack(fill_value=0)
    print(dist)

    # MODEL FEATURES
    features = df_room[CONT_VARS].copy()
    if flag_col and df_room[flag_col].sum() > 0:
        print(f"[INFO] Including HVAC flag for {name}.")
        features[f'hvac_{name}'] = df_room[flag_col]
    else:
        print(f"[INFO] HVAC off or missing for {name}.")
    if df_room['boiler_flag'].sum() > 0:
        features['boiler'] = df_room['boiler_flag']

    # TARGET
    target = df_room[f'{name}_discomfort']
    if target.nunique() < 2:
        print("[WARNING] No variation in target -> skipping model.")
        return

    # TRAIN RANDOM FOREST
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    importances = pd.Series(model.feature_importances_, index=features.columns).sort_values(ascending=False)
    print(importances)

# RUN ANALYSIS FOR EACH ROOM
for room, cols in ROOM_COLUMNS.items():
    analyze_room(room, cols)

# MULTI-ROOM DISCOMFORT
df['all_discomfort'] = df[[f'{r}_discomfort' for r in ROOM_COLUMNS]].all(axis=1)
count = df['all_discomfort'].sum()
print(f"\n[INFO] Multi-room discomfort: {count} of {len(df)} rows ({count/len(df)*100:.2f}%).")
print(f"[{datetime.now().isoformat()}] === END ===")
