#!/usr/bin/env python3
"""
MLpred2.py - Thermal Comfort Forecasting Script

License:
This software, scripts, automation examples, and code snippets authored by Cmod777 are licensed under
Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

You are free to copy, use, and adapt this software for non-commercial purposes only.
You must attribute the original author (Cmod777) and indicate any modifications.
Commercial use, redistribution for profit, or integration into proprietary products is strictly prohibited without prior permission.
See LICENSE.md for full text.
"""

import os
import sys
import logging
import requests
import json
from datetime import datetime

import pandas as pd
import numpy as np
import gspread
import joblib
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from tqdm import tqdm

# === CONFIGURATION ===
CREDS_PATH = os.path.expanduser("~/path/to/credentials.json")
SPREADSHEET_NAME = 'ANONYMIZED_SHEET'
SHEET_LEGEND = 'legend'
SHEET_INPUT = 'raw_data'
SHEET_OUTPUT = 'predictions'
TS_COLUMN = 'ts'
MODEL_DIR = os.path.expanduser("~/models/")
RETRAIN_TIMESTAMP_FILE = os.path.expanduser("~/last_retrain.txt")
TELEGRAM_TOKEN = "<YOUR_TELEGRAM_BOT_TOKEN>"
TELEGRAM_CHAT_ID = "<YOUR_CHAT_ID>"
RETRAIN_INTERVAL_HOURS = 24
RMSE_TRIGGER = 0.5
MIN_PREML2_RECORDS = 2
GRID_PARAMS = {"n_estimators": [50, 100, 200], "max_depth": [5, 10, None]}
GRID_SCORING = "neg_mean_squared_error"
GRID_CV = 3
WINDOW_SIZE = 1000  # number of rows to aggregate for prediction

# === LOGGING SETUP ===
def setup_logging():
    for f in ["mlpred2.log", "mlpred2.error.log"]:
        with open(f, 'a', encoding='utf-8') as fh:
            fh.write(f"[=== LOG START {datetime.now().isoformat()} ===]\n")
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("mlpred2.log"),
            logging.FileHandler("mlpred2.error.log")
        ]
    )

setup_logging()
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(os.path.dirname(RETRAIN_TIMESTAMP_FILE), exist_ok=True)

# === TELEGRAM NOTIFICATION ===
def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
            timeout=10
        )
    except Exception as e:
        logging.error(f"Telegram error: {e}")

# === GOOGLE SHEETS AUTH ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
client = gspread.authorize(creds)

# === TARGET-BASE MAPPING ===
target_mapping = {
    'living_room': ('comfort_lr', 'base_comfort_lr'),
    'bedroom':    ('comfort_br', 'base_comfort_br'),
    'bathroom':   ('comfort_ba', 'base_comfort_ba')
}

# === LOAD WORKSHEETS ===
def load_sheets():
    sheet = client.open(SPREADSHEET_NAME)
    legend_ws = sheet.worksheet(SHEET_LEGEND)
    input_ws = sheet.worksheet(SHEET_INPUT)
    if SHEET_OUTPUT in [w.title for w in sheet.worksheets()]:
        output_ws = sheet.worksheet(SHEET_OUTPUT)
    else:
        output_ws = sheet.add_worksheet(title=SHEET_OUTPUT, rows=100, cols=20)
    return legend_ws, input_ws, output_ws

# === READ FEATURE CODES ===
def get_feature_codes(legend_ws):
    df_leg = pd.DataFrame(legend_ws.get_all_records())
    if 'include' not in df_leg.columns or 'column_code' not in df_leg.columns:
        raise KeyError("Legend sheet must contain 'include' and 'column_code'.")
    codes = df_leg.loc[df_leg['include'].astype(str).str.upper()=='YES','column_code'].astype(str).tolist()
    if TS_COLUMN in codes:
        codes.remove(TS_COLUMN)
    return codes

# === LOAD & CLEAN DATA ===
def load_data(input_ws, codes):
    rows = input_ws.get_all_values()
    hdr = rows[0]
    if TS_COLUMN not in hdr:
        raise KeyError(f"Timestamp column '{TS_COLUMN}' not found.")
    data = rows[3:]
    df = pd.DataFrame(data, columns=hdr)
    df[TS_COLUMN] = pd.to_datetime(df[TS_COLUMN], errors='coerce', utc=True)
    df.dropna(subset=[TS_COLUMN], inplace=True)
    df.set_index(TS_COLUMN, inplace=True)
    df.sort_index(inplace=True)
    df = df[[c for c in codes if c in df.columns]]
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)
    if df.empty:
        raise ValueError("No valid data after cleaning.")
    return df

# === MODEL TRAINING & PREDICTION ===
def optimize_rf(X, y):
    grid = GridSearchCV(RandomForestRegressor(random_state=42), GRID_PARAMS,
                        scoring=GRID_SCORING, cv=GRID_CV, verbose=2, n_jobs=-1)
    grid.fit(X, y)
    logging.info(f"Best params: {grid.best_params_}")
    return grid.best_estimator_

def train_and_predict(df, target, features, name, hours=12, window_size=WINDOW_SIZE):
    path = os.path.join(MODEL_DIR, f"{name}.pkl")
    if os.path.exists(path):
        model = joblib.load(path)
    else:
        model = optimize_rf(df[features], df[target])
        joblib.dump(model, path)
    window = df[features].tail(window_size)
    Xp = window.mean().to_frame().T
    print(f"Using last {window_size} rows aggregated for prediction:")
    print(Xp.to_string(index=False))
    try:
        pred = model.predict(Xp)[0]
    except ValueError:
        model = optimize_rf(df[features], df[target])
        joblib.dump(model, path)
        pred = model.predict(Xp)[0]
    fut = df.index[-1] + pd.Timedelta(hours=hours)
    acc, hit = None, 'N/A'
    if fut in df.index:
        real = df.at[fut, target]
        if not pd.isna(real):
            err = abs(real - pred)
            acc = 1 - err/(abs(real)+0.01)
            hit = 'YES' if err < 1 else 'NO'
    y_true = df[target]
    y_pred = model.predict(df[features])
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(((y_true - y_pred)**2).mean())
    logging.info(f"{name}: MAE={mae:.2f}, RMSE={rmse:.2f}")
    if mae>RMSE_TRIGGER or rmse>RMSE_TRIGGER:
        send_telegram(f"[WARN] {name} MAE={mae:.2f}, RMSE={rmse:.2f}")
    return pred, acc, hit, mae, rmse

# === OUTPUT FUNCTIONS ===
def write_output(ws, row):
    h=list(row.keys()); v=list(row.values()); allv=ws.get_all_values()
    if not allv or allv[0]!=h: ws.append_row(h)
    ws.append_row(v)

def log_preml2(ts, zone, pred, real=None):
    sh=client.open(SPREADSHEET_NAME)
    try: ws=sh.worksheet('preML2')
    except: ws=sh.add_worksheet('preML2',100,20); ws.append_row(['timestamp','zone','prediction','real','error'])
    err=abs(real-pred) if real is not None else ''
    ws.append_row([ts,zone,round(pred,2),real if real else '',round(err,2) if real else ''])

def clean_preml2(max_rows=1000):
    try:
        ws=client.open(SPREADSHEET_NAME).worksheet('preML2')
        vals=ws.get_all_values()
        if len(vals)>max_rows+1: ws.resize(rows=max_rows+1)
    except: pass

# === RETRAIN CHECK ===
def should_retrain():
    try: last=datetime.fromisoformat(open(RETRAIN_TIMESTAMP_FILE).read().strip())
    except: last=datetime.min
    if (datetime.now()-last).total_seconds()/3600>=RETRAIN_INTERVAL_HOURS:
        return True,'time',None
    try:
        dfp=pd.DataFrame(client.open(SPREADSHEET_NAME).worksheet('preML2').get_all_records())
        dfp=dfp[pd.to_numeric(dfp['error'],errors='coerce').notna()]
        if len(dfp)>=MIN_PREML2_RECORDS:
            rmse=np.sqrt((dfp['error'].astype(float)**2).mean())
            if rmse>RMSE_TRIGGER: return True,'error',rmse
    except: pass
    return False,None,None

# === RETRAIN MODELS ===
def retrain_models():
    leg,inp,_=load_sheets()
    codes=get_feature_codes(leg)
    df=load_data(inp,codes)
    feats=[c for c in codes if c not in ['comfort_lr','comfort_br','comfort_ba']]
    for zone,target in [('living_room','comfort_lr'),('bedroom','comfort_br'),('bathroom','comfort_ba')]:
        model=optimize_rf(df[feats],df[target])
        joblib.dump(model,os.path.join(MODEL_DIR,f"model_{zone}.pkl"))
        logging.info(f"Model retrained for {zone}")

# === MAIN ===
def main():
    print(f"[{datetime.now().isoformat()}] START")
    leg,inp,out=load_sheets()
    codes=get_feature_codes(leg)
    df=load_data(inp,codes)
    print("FEATURES USED:",codes)
    stats=df[codes].agg(['min','max','nunique']).transpose()
    print(stats.to_string())
    logging.info("Feature stats: "+stats.to_string())
    retrain,reason,rm=should_retrain()
    if retrain:
        retrain_models()
        open(RETRAIN_TIMESTAMP_FILE,'w').write(datetime.now().isoformat())
        send_telegram(f"Retrained due to {reason} (rmse={rm})")
    ts=df.index[-1].isoformat()
    output_row={'timestamp':ts}
    feats=[c for c in codes if c not in ['comfort_lr','comfort_br','comfort_ba']]
    for zone,(tgt,base) in tqdm(target_mapping.items(),desc='Forecast',unit='zone'):
        p,acc,hit,mae,rmse= train_and_predict(df,tgt,feats,f"model_{zone}")
        fut=df.index[-1]+pd.Timedelta(hours=12)
        real=df.at[fut,tgt] if fut in df.index else None
        log_preml2(ts,zone,p,real)
        print(f"{zone} pred={p:.2f} acc={acc} hit={hit}")
        output_row.update({
            f"pred_{zone}":round(p,2),
            f"flag_{zone}":('OK' if 20<=p<=26 else 'ALERT'),
            f"trend_{zone}":('UP' if p>df.at[df.index[-1],base] else 'DOWN'),
            f"acc_{zone}":round(acc*100,1) if acc else 'N/A',
            f"hit_{zone}":hit
        })
    write_output(out,output_row)
    clean_preml2()
    send_telegram(f"Completed {len(output_row)} fields at {ts}")
    print(f"[{datetime.now().isoformat()}] END")
    footer=f"[=== LOG END {datetime.now().isoformat()} ===]\n"+ "-"*60 + "\n\n"
    for f in ["mlpred2.log","mlpred2.error.log"]:
        with open(f,'a') as fh: fh.write(footer)

if __name__=='__main__':
    try: main()
    except Exception as e:
        logging.exception('Critical error')
        send_telegram(f"ERROR: {e}")
        sys.exit(1)
