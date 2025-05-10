# Configuration and Execution Guide for Athena.py

This guide summarizes all the steps required to configure and run the **athena.py** script.

---
## Badges

![Version](https://img.shields.io/badge/version-v1.4-blue)
![Status](https://img.shields.io/badge/status-in%20development%2Fmaintenance-yellow)
![Testing](https://img.shields.io/badge/testing-required-red)
![Build](https://img.shields.io/badge/build-unknown-lightgrey)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License Type](https://img.shields.io/badge/software%20license-CC%20BY--NC%204.0%20%2B%20custom--restriction-lightgrey)
![Docs](https://img.shields.io/badge/docs-incomplete-orange)
![Stability](https://img.shields.io/badge/stability-not%20production%20ready-red)

---

# Overview:

This script is a modular and extensible **Machine Learning pipeline** designed to:

- Load time-series or tabular data from **Google Sheets**.
- Select only the active columns declared by the user.
- Analyze the variability and structure of the data.
- Detect potential **biases** using correlation and SHAP values.
- Choose and train one or more **ML models** dynamically.
- Evaluate models using **rolling window cross-validation**.
- Log results, warnings, and predictions locally and optionally via Telegram.

---

## Main Components and Flow

### 1. **Input and Setup**
- Reads command-line arguments (`argparse`) to configure behavior.
- Connects to Google Sheets using a service account.
- Extracts relevant column codes based on the legend sheet.

### 2. **Data Analysis**
- Calculates feature variability to suggest appropriate ML models.
- Detects **correlations** between features and sensitive columns.
- Uses SHAP (SHapley values) to detect **potential model bias**.

### 3. **Model Selection and Training**
- Dynamically chooses candidate algorithms based on:
  - Data size
  - Feature types
  - Available memory
- Trains models using a **rolling time-window validation** approach.
- Tracks CPU and RAM usage during training.

### 4. **Performance Evaluation**
- Compares models based on **RMSE** and **R²** scores.
- Stores the best-performing model per zone (column).
- Applies a fallback mechanism if no good model is found.

### 5. **Postprocessing**
- Writes predictions to an output sheet or buffer.
- Sends alerts or notifications for:
  - Model bias
  - Low accuracy
  - Resource overuse

---

## Special Features

- **Modular structure**: Each logical step is encapsulated in its own block or function.
- **Bias detection**: Both statistical (correlation) and model-based (SHAP).
- **Resource monitoring**: Avoids system saturation using thresholds.
- **Interactive CLI**: Allows the user to choose models and set thresholds.
- **Telegram alerts**: (if configured) send automatic warnings and summaries.

---

## Technologies Used

- `pandas`, `numpy` for data handling
- `scikit-learn`, `xgboost`, `lightgbm`, `catboost` for modeling
- `shap` for explainability
- `psutil` for system monitoring
- `gspread` and `oauth2client` for Google Sheets API

---

## Typical Use Case

1. A user has a structured Google Sheet with environmental or energy data.
2. The script is run via CLI, possibly on a schedule (cron).
3. The system analyzes, trains, and updates predictions autonomously.
4. Warnings are logged and optionally sent to a messaging platform.

---

## Future Improvements (Planned)

- External configuration files for thresholds and options.
- Persistent model versioning and performance tracking.
- Export of predictions to Google Sheets.
- Web dashboard for result visualization.
  
---

## 1. Project Structure

Ensure your project folder (`ML/`) contains the following files and directories:

```
athena.py           # Main script
cli.py              # Command-line argument parser
config.py           # Google Sheets configuration
auth.py             # Google Sheets authentication
notifier.py         # Telegram notification functions
creds.json          # Google service account credentials
data_loader.py      # Data loading function
retrain.py          # Model retraining function
output_utils.py     # Prediction output and cleanup functions
venv/               # Python virtual environment
requirements.txt    # (optional) list of dependencies
```

---

## 2. Create the Virtual Environment

```bash
cd ML/
python3 -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate   # Windows
```

---

## 3. Install Dependencies

Install all required libraries:

```bash
pip install \
  gspread google-auth requests pandas scikit-learn xgboost shap tqdm matplotlib joblib
```

*Optional:* generate `requirements.txt` with:

```
gspread
google-auth
requests
pandas
scikit-learn
xgboost
shap
tqdm
matplotlib
joblib
```

and then:

```bash
pip install -r requirements.txt
```

---

## 4. Configuration Files

### 4.1 config.py

```python
SPREADSHEET_NAME   = "NAME1"
SHEET_LEGENDA      = "NAME2"
SHEET_INPUT        = "NAME3"
SHEET_OUTPUT       = "NAME4"
GOOGLE_CREDS_FILE  = "creds.json"
```

### 4.2 auth.py

```python
import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_CREDS_FILE

def get_spreadsheet_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(GOOGLE_CREDS_FILE, scopes=scopes)
    return gspread.authorize(creds)
```

### 4.3 notifier.py

```python
import requests
BOT_TOKEN = "<YOUR_TELEGRAM_BOT_TOKEN>"
CHAT_ID   = "<YOUR_CHAT_ID>"

def invia_notifica_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    r = requests.post(url, data=payload)
    if not r.ok:
        print("Telegram send error:", r.text)
```

### 4.4 cli.py

```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Athena ML Pipeline")
    parser.add_argument("--title", type=str, default="default", help="Log title and filename prefix")
    parser.add_argument("--target", type=str, help="Comma-separated list of target codes to process")
    parser.add_argument("--analisi_velocita", choices=["si","no"], default="no", help="Enable pattern velocity analysis")
    parser.add_argument("--disable", type=str, default="", help="Comma-separated list of blocks to disable")
    parser.add_argument("--use_benchmark", action="store_true", help="Use historical benchmark data if available")
    parser.add_argument("--benchmark_sheet", type=str, help="Worksheet name for benchmark data")
    parser.add_argument("--threshold_r2", type=float, default=0.8, help="Minimum R² threshold")
    parser.add_argument("--cv_folds", type=int, default=5, help="Number of cross-validation folds")
    parser.add_argument("--cv_k", type=float, default=1.0, help="Std penalty factor for CV threshold")
    parser.add_argument("--sensitive_cols", type=str, help="Comma-separated list of sensitive columns for bias analysis")
    return parser.parse_args()
```

### 4.5 data\_loader.py

```python
import pandas as pd

def carica_dati(input_ws, codici_attivi):
    records = input_ws.get_all_records()
    df = pd.DataFrame(records)
    df = df[[col for col in df.columns if col in codici_attivi]]
    return df
```

### 4.6 retrain.py

```python
import joblib

def riaddestra_modelli(model_path, X, y):
    model = joblib.load(model_path)
    model.fit(X, y)
    joblib.dump(model, model_path)
    return model
```

### 4.7 output\_utils.py

```python
import json

def scrivi_previsioni_preml2(timestamp, zona, previsione, extra=None):
    record = {"timestamp": timestamp, "zona": zona, "previsione": previsione, "extra": extra}
    with open('previsioni.json','a') as f:
        f.write(json.dumps(record)+"\n")

def pulisci_preml2():
    pass
```

---

## 5. Changes to athena.py

1. **Replace** the stray `return` in BLOC 7b with `sys.exit(1)`.
2. In BLOC 7c, after printing active codes, add:

   ```python
   codici_attivi = [str(c) for c in codici_attivi]
   target_map = {str(c): str(c) for c in codici_attivi}
   ```
3. In BLOC 6, update the final notification call to:

   ```python
   invia_notifica_telegram(f"Script completed at {datetime.datetime.now().isoformat()}")
   ```

---

## 6. Running the Script

```bash
python athena.py \
  --title MyRun \
  --analisi_velocita si \
  --target 100,105,110
```

* **--title**: log file prefix
* **--analisi\_velocita**: "si" to enable velocity analysis
* **--target**: codes to process
* **--disable**: skip specific blocks (e.g. `postprocess,notify`)
* Advanced options: `--use_benchmark`, `--benchmark_sheet`, `--threshold_r2`, `--cv_folds`, `--cv_k`, `--sensitive_cols`

---

## 7. Troubleshooting

* Ensure `creds.json` is in project root and matches `GOOGLE_CREDS_FILE`.
* Verify `matplotlib` and `shap` are installed for plots.
* Use `--analisi_velocita no` to skip algorithm suggestion.
* Check `previsioni.json` for output records.

---

*End of Configuration Guide.*
