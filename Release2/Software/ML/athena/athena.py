# =============================================================
#  athena.py Pipeline - Main Script
# =============================================================
#  Version      : 1.4
#  Status       : In Development / Maintenance
#  License      : Creative Commons Attribution - NonCommercial 4.0
#                 WITH supplemental clause: commercial use prohibited
#                 unless prior written authorization is granted by the author.
#  Author       : Cmod777
#  Created      : April 2025
#  Last Update  : May 2025
#  Python       : 3.10+
# =============================================================
#  DISCLAIMER
#  This script is provided for educational and non-commercial use only.
#  Commercial reproduction, resale, or integration in proprietary tools
#  is strictly forbidden without explicit authorization.
#  Use at your own risk. No warranty is provided.
# =============================================================

# BLOC 0.A - IMPORTS AND CONSTANTS
# Import modules and constants

from datetime import datetime
from cli import parse_args
from auth import get_spreadsheet_client
from config import SPREADSHEET_NAME, SHEET_LEGEND, SHEET_INPUT, SHEET_OUTPUT
from config_pipeline import *  # External thresholds and algorithm definitions
import sys
import logging

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb

from data_loader import load_data
from retrain import retrain_models
from output_utils import write_predictions, clean_preictions
from notifier import send_telegram_notification

# BLOC 0.B - LOGGING UTILITIES
# Logging configuration and formatted log output

def setup_logging(title="default"):
    """Set up basic logging configuration."""
    log_filename = f"pipeline_{title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def log_with_header_footer(logger, level, message, zone, algorithm):
    """Log a message with header and footer including zone and algorithm info."""
    timestamp = datetime.now().isoformat()
    header = f"*** START LOG ALERT for {zone} - Algorithm: {algorithm} - {timestamp} ***"
    footer = f"*** END LOG ALERT for {zone} - Algorithm: {algorithm} - {timestamp} ***"
    logger.log(level, header)
    logger.log(level, message)
    logger.log(level, footer)

# BLOC 1.A - CLI ARGUMENTS AND LOGGING
# Parse CLI arguments, configure logger

import time

args = parse_args()
disabled_blocks = args.disable.split(",") if getattr(args, "disable", None) else []
logger = setup_logging(getattr(args, "title", "default"))

# BLOC 1.B - SPREADSHEET CONNECTION WITH RETRY
# Connect to spreadsheet and get worksheets with retry logic

MAX_RETRIES = 3
RETRY_DELAY = 5  # Seconds

spreadsheet_ok = False
spreadsheet = None
legend_ws = None
input_ws = None
output_ws = None

for attempt in range(1, MAX_RETRIES + 1):
    print(f"Trying to connect to spreadsheet (attempt {attempt}/{MAX_RETRIES})...")
    try:
        client = get_spreadsheet_client()
        spreadsheet = client.open(SPREADSHEET_NAME)
        legend_ws = spreadsheet.worksheet(SHEET_LEGEND)
        input_ws = spreadsheet.worksheet(SHEET_INPUT)
        sheet_out_name = args.sheet_output if args.sheet_output else SHEET_OUTPUT
        output_ws = spreadsheet.worksheet(sheet_out_name)

        logger.info(f"Successfully connected to spreadsheet '{SPREADSHEET_NAME}' on attempt {attempt}.")
        spreadsheet_ok = True
        break
    except Exception as e:
        send_alert("error", f"Connection attempt {attempt}/{MAX_RETRIES} failed: {e}")
        print(f"Connection error (attempt {attempt}/{MAX_RETRIES}). Retrying in {RETRY_DELAY} seconds...")
        time.sleep(RETRY_DELAY)

if not spreadsheet_ok:
    print(f"Unable to connect to spreadsheet '{SPREADSHEET_NAME}' after {MAX_RETRIES} attempts. Exiting.")
    sys.exit(1)

# BLOC 1.C - EXTRACT ACTIVE COLUMN CODES FROM LEGEND
# Parse column codes from the legend worksheet

active_codes = []

if spreadsheet_ok and legend_ws:
    print("Extracting active column codes from legend...")
    try:
        for row in legend_ws.get_all_records():
            code = row.get("column_code")
            include = row.get("include", "NO").upper()
            if code and include == "YES":
                active_codes.append(code)

        logger.info(f"Active column codes extracted: {active_codes}")
        print(f"Active column codes: {active_codes}")
        print(f"Selected zones (targets): {args.target.split(',') if args.target else 'all'}")
    except Exception as e:
        send_alert("error", f"Error extracting active column codes: {e}")
        print("Error extracting active column codes from legend.")
        active_codes = []
else:
    send_alert("warning", "Legend worksheet unavailable. Cannot extract active codes.")

# BLOC 1.D - MODEL VALIDATION PARAMETERS
# Extract model threshold and CV parameters from CLI

use_benchmark = getattr(args, "use_benchmark", False)
benchmark_sheet = getattr(args, "benchmark_sheet", None)
threshold_r2 = getattr(args, "threshold_r2", THRESHOLD_R2_DEFAULT)
cv_folds = getattr(args, "cv_folds", CV_FOLDS_DEFAULT)
cv_k = getattr(args, "cv_k", CV_K_DEFAULT)

# BLOC 2.A - DATA VARIABILITY ANALYSIS AND ALGORITHM SUGGESTION
# Analyze feature variability and suggest the most suitable ML algorithm

# Thresholds moved to config_pipeline.py

def analyze_velocity(df):
    """
    Analyze the rate of change of features in a DataFrame
    and suggest a suitable ML algorithm based on variability.
    """
    numeric_df = df.select_dtypes(include='number')
    diffs = numeric_df.diff().abs()
    mean_velocity = diffs.mean()

    logger.info(f"Mean velocity per feature: {mean_velocity.to_dict()}")

    numeric_cols = df.select_dtypes(include='number')
    categorical_cols = df.select_dtypes(exclude='number')
    avg_std = numeric_cols.std().mean() if not numeric_cols.empty else 0
    avg_cardinality = categorical_cols.nunique().mean() if not categorical_cols.empty else 0

    if not categorical_cols.empty and avg_cardinality > AVG_CARDINALITY_THRESHOLD:
        suggestion = 'random_forest'
    elif avg_std < VELOCITY_THRESHOLD_LOW:
        suggestion = 'linear_regression'
    elif avg_std > VELOCITY_THRESHOLD_HIGH:
        suggestion = 'xgboost'
    else:
        suggestion = 'gradient_boosting'

    logger.info(f"Suggested algorithm: {suggestion}")
    return suggestion

# BLOC 2.B - SMART MODEL SELECTION BASED ON CONTEXT
# Suggest candidate models based on data size and available resources

import psutil

def select_smart_models(df, prediction_hours=3):
    """
    Analyze data and machine resources to suggest an ordered list of ML models.
    """
    row_count = len(df)
    free_ram_mb = psutil.virtual_memory().available / 1024**2
    has_categorical = not df.select_dtypes(exclude='number').empty

    models = []
    models.append(("LinearRegression", 1))

    if free_ram_mb > 50:
        models.append(("Ridge", 2))
    if row_count < 1000 and free_ram_mb > 100:
        models.append(("RandomForest", 3))
    if row_count < 1000 and free_ram_mb > 150:
        models.append(("GradientBoosting", 4))
    if row_count < 500 and free_ram_mb > 300 and not has_categorical:
        models.append(("XGBoost", 5))
    if row_count < 700 and free_ram_mb > 250:
        models.append(("LightGBM", 6))
    if row_count < 500 and free_ram_mb > 150:
        models.append(("SVR", 7))
    if row_count < 500 and free_ram_mb > 200:
        models.append(("KNN", 8))
    if has_categorical and free_ram_mb > 400:
        models.append(("CatBoost", 9))

    sorted_models = sorted(models, key=lambda x: x[1])
    print("\n[INFO] Suggested models (ordered):")
    for name, priority in sorted_models:
        print(f"  [{priority}] {name}")

    return [name for name, _ in sorted_models]

# BLOC 3.A - LOAD AND VALIDATE INPUT DATA
# Begin operational phase: data is loaded and checked before training

from tqdm import tqdm
import pandas as pd

def load_and_validate_data(input_ws, active_codes):
    """Load data from worksheet and validate expected columns."""
    logger.info("BLOCK 3.A: DATA LOADING AND INITIAL SETUP")
    print("\n=== BLOCK 3.A: DATA LOADING AND INITIAL SETUP ===")
    print("Loading data...")

    df = load_data(input_ws, active_codes)

    if df is None or df.empty:
        send_alert("error", "Data load failed or DataFrame is empty.")
        print("Error: Data load failed or DataFrame is empty.")
        return None

    missing_cols = [col for col in active_codes if col not in df.columns]
    if missing_cols:
        send_alert("error", f"Missing active columns in loaded DataFrame: {missing_cols}")
        print(f"Error: Missing active columns: {missing_cols}")
        return None

    if not active_codes:
        logger.warning("No active column codes found in legend.")
        print("Warning: No active column codes found. Training will be skipped.")
        return None

    print("Data loading completed.")
    return df

# BLOC 3.B - CORRELATION ANALYSIS: INPUT VALIDATION
# Validate DataFrame and isolate non-sensitive features

import pandas as pd
import numpy as np
from logging import getLogger

logger = getLogger(__name__)

def analyze_sensitivity_correlation(df, sensitive_cols=None):
    """Analyze feature sensitivity through correlation with specified columns."""
    logger.info("BLOCK 3.B: CORRELATION SENSITIVITY ANALYSIS")
    print("\n=== BLOCK 3.B: CORRELATION SENSITIVITY ANALYSIS ===")

    sensitive_correlations = {}
    # SENSITIVITY_CORRELATION_THRESHOLD moved to config_pipeline.py
    bias_detected_corr = False

    if df is None or df.empty or not sensitive_cols:
        print("Warning: DataFrame is empty or no sensitive columns specified for correlation.")
        return sensitive_correlations, bias_detected_corr

    feature_cols = [col for col in df.columns if col not in sensitive_cols]
    if not feature_cols:
        print("Warning: No features available for correlation analysis.")
        return sensitive_correlations, bias_detected_corr

# BLOC 3.C - CORRELATION ANALYSIS: PROCESSING
# Iterate features and compute correlations with sensitive columns

    print("Analyzing feature sensitivity using correlation...")

    for sensitive_col in sensitive_cols:
        if sensitive_col in df.columns:
            sensitive_correlations[sensitive_col] = {}

            for feature_col in feature_cols:
                if pd.api.types.is_numeric_dtype(df[feature_col]) and pd.api.types.is_numeric_dtype(df[sensitive_col]):
                    corr = df[feature_col].corr(df[sensitive_col])

                    if abs(corr) > SENSITIVITY_CORRELATION_THRESHOLD:
                        bias_detected_corr = True

                        if feature_col not in sensitive_correlations[sensitive_col]:
                            sensitive_correlations[sensitive_col][feature_col] = []

                        sensitive_correlations[sensitive_col][feature_col].append(f"Correlation: {corr:.2f}")
                        print(f"  Sens. Col: '{sensitive_col}', Feature: '{feature_col}' - Correlation: {corr:.2f}")
                        send_telegram_notification(
                            f"**POTENTIAL BIAS WARNING (Correlation):**\n"
                            f"Significant correlation ({corr:.2f}) found between feature '{feature_col}' and sensitive column '{sensitive_col}'."
                        )

# BLOC 3.D - CORRELATION ANALYSIS: OUTPUT
# Print and return correlation results

    if sensitive_correlations:
        send_alert("warning", f"Potential feature-sensitivity correlations: {sensitive_correlations}", notify=True)
        print(f"Warning: Potential correlations found: {sensitive_correlations}")
    else:
        print("No significant correlations detected with the specified sensitive columns.")

    return sensitive_correlations, bias_detected_corr

# BLOC 4.A - HANDLE BIAS WARNING
# Display warning if bias is detected and prepare initial algorithm list

def handle_bias_warning(suggested_algo, bias_detected):
    """Handle potential bias warning and prepare algorithm list."""
    bias_alert = bias_detected
    algos_to_run = [suggested_algo]

    if bias_alert:
        print("\nWARNING: Potential bias detected in the suggested model (via correlation or SHAP).")
        print(f"Suggested algorithm: {suggested_algo}")
        print("Consider using alternative algorithms to mitigate bias.")
    else:
        print(f"Recommended algorithm: {suggested_algo}")

    return bias_alert, algos_to_run

# BLOC 4.B - SELECT ALGORITHMS
# Allow manual or automatic selection of algorithms, based on bias and interaction

def select_algorithms(suggested_algo, bias_alert, algos_to_run):
    """Allow manual or automatic selection of algorithms."""
    if bias_alert:
        if sys.stdin.isatty():
            ask_more = input("Do you want to manually select which algorithms to run? [Y/n]: ")
            if ask_more.lower() in ["", "y", "yes"]:
                choices = ["linear_regression", "random_forest", "xgboost", "gradient_boosting", "all"]
                print("Choose algorithms:")
                for i, opt in enumerate(choices, 1):
                    print(f" [{i}] {opt}")
                selected_indices = input("Enter numbers of algorithms (comma-separated), or 'all': ")
                if selected_indices.lower() == "all":
                    algos_to_run = choices[:-1]
                else:
                    algos_to_run = []
                    selected_indices_list = [s.strip() for s in selected_indices.split(',')]
                    for sel in selected_indices_list:
                        try:
                            idx = int(sel) - 1
                            if 0 <= idx < len(choices) - 1:
                                algos_to_run.append(choices[idx])
                            elif idx == len(choices) - 1:
                                algos_to_run = choices[:-1]
                                break
                            else:
                                print(f"Invalid selection: {sel}")
                        except ValueError:
                            print(f"Invalid input: {sel}")
                    if not algos_to_run:
                        algos_to_run = [suggested_algo]
                        print(f"No valid algorithms selected, using suggested: {suggested_algo}")
            else:
                if suggested_algo == "linear_regression":
                    algos_to_run.append("random_forest")
                elif suggested_algo == "random_forest":
                    algos_to_run.append("linear_regression")
                elif suggested_algo == "xgboost":
                    algos_to_run.append("gradient_boosting")
                elif suggested_algo == "gradient_boosting":
                    algos_to_run.append("xgboost")
                algos_to_run = list(set(algos_to_run))
                print(f"Automatically added alternative algorithm: {algos_to_run[1]}")
        else:
            if suggested_algo == "linear_regression":
                algos_to_run.append("random_forest")
            elif suggested_algo == "random_forest":
                algos_to_run.append("linear_regression")
            elif suggested_algo == "xgboost":
                algos_to_run.append("gradient_boosting")
            elif suggested_algo == "gradient_boosting":
                algos_to_run.append("xgboost")
            algos_to_run = list(set(algos_to_run))
            print(f"Non-interactive mode: bias detected, running: {algos_to_run}")
    elif sys.stdin.isatty():
        use_default = input("Do you want to use the suggested algorithm? [Y/n]: ")
        if use_default.lower() not in ["", "y", "yes"]:
            choices = ["linear_regression", "random_forest", "xgboost", "gradient_boosting", "all"]
            print("Choose algorithm:")
            for i, opt in enumerate(choices, 1):
                print(f" [{i}] {opt}")
            sel = input("Enter number: ")
            try:
                idx = int(sel) - 1
                if idx == 4:
                    algos_to_run = choices[:-1]
                elif 0 <= idx < 4:
                    algos_to_run = [choices[idx]]
                else:
                    logger.warning(f"Invalid algorithm choice, using suggested: {suggested_algo}")
                    print(f"Invalid choice, using suggested: {suggested_algo}")
            except ValueError:
                logger.warning(f"Invalid input, using suggested: {suggested_algo}")
                print(f"Invalid input, using suggested: {suggested_algo}")
    else:
        algos_to_run = [suggested_algo]
        print(f"Non-interactive mode, using: {suggested_algo}")

    return algos_to_run, bias_alert

# BLOC 4.C - INITIAL ALGORITHM SELECTION
# Wrapper that combines bias handling and algorithm selection

def initial_algorithm_choice(suggested_algo, bias_detected):
    bias_alert, initial_algos = handle_bias_warning(suggested_algo, bias_detected)
    final_algos, final_bias_alert = select_algorithms(suggested_algo, bias_alert, initial_algos)
    return final_algos, final_bias_alert

# BLOC 4.D - LOAD BENCHMARK DATA
# Load historical R² values from benchmark sheet

def load_benchmark(spreadsheet, use_benchmark, benchmark_sheet):
    """Load benchmark history if enabled."""
    best_history = {}
    if use_benchmark and benchmark_sheet and spreadsheet:
        ws_bench = spreadsheet.worksheet(benchmark_sheet)
        print("Loading benchmark history...")
        for rec in ws_bench.get("A1:Z"):
            if rec and len(rec) >= 2 and rec[0] is not None and rec[1] is not None:
                try:
                    best_history[rec[0]] = float(rec[1])
                except ValueError:
                    send_alert("warning", f"Invalid R² in benchmark for zone '{rec[0]}': '{rec[1]}'", notify=True)
                    print(f"Warning: Invalid R² value for zone '{rec[0]}'.")
            elif rec:
                send_alert("warning", f"Incomplete or invalid benchmark row: {rec}", notify=True)
                print(f"Warning: Incomplete or invalid benchmark row.")
        print("Benchmark loaded.")
    elif use_benchmark and not benchmark_sheet:
        print("Warning: use_benchmark is enabled but benchmark_sheet is not set.")
        send_alert("warning", "use_benchmark is enabled but benchmark_sheet is not set.")
    elif benchmark_sheet and not use_benchmark:
        print("Warning: benchmark_sheet is set but use_benchmark is disabled.")
        send_alert("warning", "benchmark_sheet is set but use_benchmark is disabled.")
    return best_history

# BLOC 4.E - PLACEHOLDER FOR FUTURE EXTENSIONS
# Reserved for additional algorithm-related logic (currently empty)

pass

# BLOC 5.A - MODEL TRAINING AND EVALUATION
# Fit model, calculate R², log performance and update best result

def train_and_evaluate(algo, model, X, y, zone, logger, threshold_r2, thr_eff, best_r2_zone, best_algo_zone, best_pred_zone, results):
    r2 = -float('inf')
    y_pred = None
    alerts = []

    try:
        model.fit(X, y)
        from sklearn.metrics import r2_score
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)

        logger.info(f"{zone} [{algo}]: R² = {r2:.2f}")
        print(f"    R² on full dataset: {r2:.2f}")

        results[zone].setdefault(algo, {})["r2"] = r2
        results[zone].setdefault(algo, {})["prediction"] = y_pred[-1]

        if r2 < threshold_r2:
            alert_msg = f"**WARNING:** Performance below threshold (R²={r2:.2f} < {threshold_r2:.2f})"
            send_alert("warning", alert_msg, zone=zone, algo=algo, notify=True)
alerts.append(alert_msg)

        if r2 > best_r2_zone:
            best_r2_zone = r2
            best_algo_zone = algo
            best_pred_zone = y_pred[-1]

    except Exception as e:
        send_alert("error", f"Error during training/evaluation: {e}", zone=zone, algo=algo)
        print(f"    Error during training/evaluation.")
        alerts.append(f"Training/evaluation error: {e}")

    if alerts:
        results[zone].setdefault(algo, {})["alerts"] = alerts

    return r2, y_pred, best_r2_zone, best_algo_zone, best_pred_zone

# BLOC 5.B - FEATURE IMPORTANCE AND SHAP COMPUTATION
# Compute feature importances and SHAP values, generate plots if needed

import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

def compute_feature_importance_shap(algo, model, X, zone, logger, r2, threshold_r2):
    feature_importance_shap = None
    shap_values = None

    try:
        if algo in ["random_forest", "xgboost", "gradient_boosting"] and hasattr(model, 'feature_importances_'):
            importance = pd.DataFrame(zip(X.columns, model.feature_importances_), columns=['Feature', 'Importance']).sort_values(by='Importance', ascending=False)
            logger.info(f"{zone} - {algo} Feature Importance:\n{importance.head().to_string()}")
            print(f"    {algo} Feature Importance:\n{importance.head()}")

        try:
            explainer_shap = shap.Explainer(model, X)
            shap_values = explainer_shap(X)
            mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
            feature_importance_shap = pd.DataFrame(list(zip(X.columns, mean_abs_shap)), columns=['Feature', 'SHAP Importance']).sort_values(by='SHAP Importance', ascending=False)

            logger.info(f"{zone} - {algo} SHAP Importance:\n{feature_importance_shap.head().to_string()}")
            print(f"    {algo} SHAP Importance:\n{feature_importance_shap.head()}")

            if r2 > threshold_r2 - 0.05:
                shap.summary_plot(shap_values, features=X, show=False)
                plt.title(f"{zone} - SHAP Summary Plot ({algo})")
                plt.savefig(f"shap_summary_{zone}_{algo}.png")
                plt.close()
                logger.info(f"{zone} - SHAP Summary Plot saved.")
                print(f"  {zone} - SHAP Summary Plot generated.")

        except Exception as e_shap:
            logger.error(f"SHAP error for {algo} - zone {zone}: {e_shap}")
            print(f"  SHAP computation error.")

    except Exception as e:
        logger.error(f"Feature importance error for {algo} - zone {zone}: {e}")
        print(f"  Feature importance computation error.")

    return feature_importance_shap, shap_values

# BLOC 5.C - BIAS ANALYSIS VIA SHAP
# Compare SHAP values across groups and log potential bias

def analyze_bias(algo, X, zone, logger, feature_importance_shap, shap_values, bias_detected_corr, results):
    bias_analysis_successful = False
    alerts = results.setdefault(zone, {}).setdefault(algo, {}).setdefault("alerts", [])

    if X is not None and feature_importance_shap is not None and shap_values is not None:
        try:
            top_features = feature_importance_shap['Feature'].head(3).tolist()
            for feature in top_features:
                if feature in X.columns:
                    median_val = X[feature].median()
                    group_low = X[X[feature] <= median_val]
                    group_high = X[X[feature] > median_val]

                    if not group_low.empty and not group_high.empty:
                        shap_low = shap_values[group_low.index].values[:, X.columns.get_loc(feature)].mean()
                        shap_high = shap_values[group_high.index].values[:, X.columns.get_loc(feature)].mean()
                        difference = abs(shap_high - shap_low)

                        if difference > 0.05:
                            alert_msg = f"**POTENTIAL BIAS DETECTED:** Difference in impact of '{feature}' between groups (diff={difference:.4f})"
                            send_alert("warning", alert_msg, zone=zone, algo=algo, notify=True)
                            alerts.append(alert_msg)
                            bias_analysis_successful = True
                            break

        except Exception as e:
            alert_msg = f"Error in SHAP-based bias analysis: {e}"
            send_alert("warning", alert_msg, zone=zone, algo=algo, notify=True)
            alerts.append(alert_msg)

    if not bias_analysis_successful:
        send_alert("info", "SHAP bias analysis failed. Using fallback.", zone=zone, algo=algo)
        if bias_detected_corr:
            alert_msg = "**POTENTIAL CORRELATION BIAS:** Check features correlated with sensitive variables."
            send_alert("warning", alert_msg, zone=zone, algo=algo, notify=True)
            alerts.append(alert_msg)
        else:
            send_alert("info", "No fallback bias indicators detected.", zone=zone, algo=algo)

    if alerts:
        results[zone][algo]["alerts"] = alerts

# BLOCK 5.D sec 1 - MAIN TRAINING LOOP FOR ALGORITHM - SECTION 1: Initialization and Resource Monitoring
# Iterate over algorithms: monitor resources and attempt cross-validation

import psutil
import numpy as np
from sklearn.model_selection import train_test_split
import time
from sklearn.metrics import mean_squared_error

# BLOCK 5.D sec 1 - sub-section A - USER INTERFACE FOR DATA TYPE SELECTION

print("Tell me more about the data you will use for the prediction (besides date/time):")
print("[1] Mostly numbers that can have decimals (e.g., temperatures, sales, measurements)")
print("[2] Mostly values that are only 0 or 1 (e.g., on/off, yes/no)")
print("[3] Mostly whole numbers that represent categories or choices (e.g., product type: 1=A, 2=B, 3=C)")
print("[4] A mix of different data types (numbers with decimals, 0/1, whole numbers representing categories)")
print("[0] Not sure / My data is complex")
data_type_choice = input("Enter the corresponding number (or 0 if not sure): ")

if data_type_choice == "1":
    algos_to_run_ordered = ["lightgbm", "xgboost", "gradient_boosting", "random_forest", "linear_regression", "svr", "knn", "catboost"]
elif data_type_choice == "2":
    algos_to_run_ordered = ["lightgbm", "xgboost", "random_forest", "gradient_boosting", "linear_regression", "svr", "knn", "catboost"]
elif data_type_choice == "3":
    algos_to_run_ordered = ["lightgbm", "catboost", "xgboost", "random_forest", "gradient_boosting", "linear_regression", "svr", "knn"]
elif data_type_choice == "4":
    algos_to_run_ordered = algos_to_run
elif data_type_choice == "0":
    algos_to_run_ordered = algos_to_run
else:
    send_alert("warning", "Invalid choice in data type selection. Using default algorithm order.")
    algos_to_run_ordered = algos_to_run

# Now we use the ordered list for iteration
for algo in algos_to_run_ordered:
    logger.info(f"Attempting algorithm: {algo}")
    print(f"  Attempting algorithm: {algo}")
    model = None

    max_ram_threshold = getattr(args, "max_ram_percentage", MAX_RAM_PERCENTAGE_DEFAULT)
    max_cpu_threshold = getattr(args, "max_cpu_percentage", MAX_CPU_PERCENTAGE_DEFAULT)

    if max_ram_threshold > MAX_RAM_PERCENTAGE_DEFAULT or max_cpu_threshold > MAX_CPU_PERCENTAGE_DEFAULT:
        send_alert("warning", "Configured resource thresholds are higher than recommended defaults.", zone=zone, algo=algo)

    high_resource_counter = 0
    critical_resource_counter = 0
    exceeded_resources = False

    if algo == "linear_regression":
        model = LinearRegression()
    elif algo == "random_forest":
        model = RandomForestRegressor()
    elif algo == "xgboost":
        model = xgb.XGBRegressor()
    elif algo == "gradient_boosting":
        model = GradientBoostingRegressor()
    elif algo == "lightgbm":
        from lightgbm import LGBMRegressor
        model = LGBMRegressor()
    elif algo == "svr":
        from sklearn.svm import SVR
        model = SVR()
    elif algo == "knn":
        from sklearn.neighbors import KNeighborsRegressor
        model = KNeighborsRegressor()
    elif algo == "catboost":
        from catboost import CatBoostRegressor
        model = CatBoostRegressor(verbose=0)
    else:
        send_alert("warning", f"Unrecognized algorithm '{algo}'. Skipping.", zone=zone)
        continue

# BLOCK 5.D sec 1 - sub-section B: Implementing Time Series Rolling Window Validation ---
    total_rows = len(X)
    num_cycles = 5
    fold_size = total_rows // 6
    cycle_performances = []

    start_time_cv = time.time()

    while True:  # Keep while True for resource monitoring
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        logger.info(f"{zone} - {algo}: CPU Usage = {cpu_percent}%, RAM Usage = {ram_percent}%")

        if cpu_percent > max_cpu_threshold or ram_percent > max_ram_threshold:
            high_resource_counter += RESOURCE_MONITORING_INTERVAL
            if high_resource_counter >= HIGH_RESOURCE_THRESHOLD_DURATION:
                send_alert(
                    "warning",
                    f"High resource usage (CPU > {max_cpu_threshold}%, RAM > {max_ram_threshold}%) for {HIGH_RESOURCE_THRESHOLD_DURATION} seconds. Potential saturation risk.",
                    zone=zone,
                    algo=algo,
                    notify=True
                )
                critical_resource_counter += RESOURCE_MONITORING_INTERVAL
                if critical_resource_counter >= CRITICAL_RESOURCE_THRESHOLD_DURATION:
                    send_alert(
                        "error",
                        f"Critical resource usage exceeded for {CRITICAL_RESOURCE_THRESHOLD_DURATION + HIGH_RESOURCE_THRESHOLD_DURATION} seconds. Stopping current algorithm '{algo}'.",
                        zone=zone,
                        algo=algo,
                        notify=True
                    )
                    exceeded_resources = True
                    break
        else:
            high_resource_counter = 0
            critical_resource_counter = 0

        for i in range(num_cycles):
            train_start = 0
            train_end = (i + 1) * fold_size
            predict_start = train_end
            predict_end = min((i + 2) * fold_size, total_rows)

            if predict_start >= total_rows:
                break

            X_train_temp = X[train_start:train_end]
            y_train_temp = y[train_start:train_end]
            X_predict_temp = X[predict_start:predict_end]
            y_true_temp = y[predict_start:predict_end]

            try:
                model.fit(X_train_temp, y_train_temp)
                predictions_temp = model.predict(X_predict_temp)

                rmse = np.sqrt(mean_squared_error(y_true_temp, predictions_temp))
                cycle_performances.append(rmse)
                logger.info(f"{zone} - {algo}: Temporal CV Cycle {i+1} RMSE = {rmse:.4f}")
                print(f"  {algo}: Temporal CV Cycle {i+1} RMSE = {rmse:.4f}")

            except Exception as e:
                send_alert(
                    "error",
                    f"{zone} - {algo}: Error during temporal CV cycle {i+1}: {e}",
                    zone=zone,
                    algo=algo
                )
                print(f"  {algo}: Error during temporal CV cycle {i+1}: {e}")
                cycle_performances.append(np.nan)

            time.sleep(RESOURCE_MONITORING_INTERVAL)

        end_time_cv = time.time()
        cv_time = end_time_cv - start_time_cv
        mean_rmse = np.nanmean(cycle_performances)
        logger.info(f"{zone} - {algo}: Temporal CV completed in {cv_time:.2f} seconds. Mean RMSE = {mean_rmse:.4f}")
        print(f"  {algo}: Temporal CV completed in {cv_time:.2f} seconds. Mean RMSE = {mean_rmse:.4f}")

        # Invert sign for consistency with previous logic (though lower RMSE is better here)
        thr_cv = -mean_rmse

        # May need to adapt 'thr_cv' logic if used elsewhere for selection.
        # For now, directly store mean_rmse in results.
        results[zone][algo] = {
            "temporal_cv_rmse_mean": mean_rmse,
            "temporal_cv_rmse_cycles": cycle_performances,
            "temporal_cv_time": cv_time
        }

        exceeded_resources = False
        break
# --- END OF: Implementing Time Series Rolling Window Validation ---


# BLOCK 5.D sec 2 - MAIN TRAINING LOOP FOR ALGORITHM - SECTION 2: Handling Interruption and Training/Evaluation
# Handle resource exceeding and proceed with training/evaluation if no interruption

    if exceeded_resources and sys.stdin.isatty():
        print(f"\nHigh resource usage with algorithm '{algo}'. What would you like to do?")
        options = ["Reduce dataset (%)", "Try a lighter algorithm", "Skip this algorithm"]
        for i, option in enumerate(options):
            print(f"[{i+1}] {option}")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            while True:
                try:
                    reduction_percent = float(input("Enter the percentage to reduce the dataset (e.g., 0.8 for 80%): "))
                    if 0 < reduction_percent < 1:
                        X_reduced, _, y_reduced, _ = train_test_split(X, y, train_size=reduction_percent, random_state=42) # Reduce the dataset
                        X, y = X_reduced, y_reduced # Update X and y with the reduced dataset
                        logger.info(f"{zone}: Dataset reduced to {reduction_percent*100}% for algorithm '{algo}'.") # Log dataset reduction
                        print(f"  Dataset reduced. Retrying cross-validation for '{algo}'.") # Print info about retrying
                        high_resource_counter = 0 # Reset resource counters after data reduction
                        critical_resource_counter = 0
                        exceeded_resources = False # Reset the flag
                        break
                    else:
                        print("Please enter a percentage between 0 and 1 (exclusive).")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == "2":
            lighter_algorithms = [alg for alg in algos_to_run if alg != algo] # Suggest other algorithms
            if lighter_algorithms:
                print("Consider trying one of these lighter algorithms:", lighter_algorithms)
            else:
                print("No other algorithms available to try.")
            continue # Skip to the next algorithm
        elif choice == "3":
            print(f"Skipping algorithm '{algo}'.")
            logger.info(f"{zone}: Skipping algorithm '{algo}' due to resource issues.") # Log skipping
            continue # Skip to the next algorithm
        else:
            print("Invalid choice. Skipping this algorithm.")
            send_alert("warning", f"Invalid user choice for resource handling. Skipping '{algo}'.", zone=zone, algo=algo) # Log invalid choice
            continue # Skip to the next algorithm

    if not exceeded_resources:
        logger.info(f"{zone} - {algo}: Starting final training and evaluation.")
        print(f"  Starting final training and evaluation for '{algo}'.")
        start_time = time.time()
        model.fit(X, y) # Train the model on the full dataset (or reduced if user chose to)
        end_time = time.time()
        training_time = end_time - start_time
        logger.info(f"{zone} - {algo}: Training completed in {training_time:.2f} seconds.")
        print(f"    Training completed in {training_time:.2f} seconds.")

        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        logger.info(f"{zone} - {algo}: R² = {r2:.4f}, RMSE = {rmse:.4f}")
        print(f"    R² on test set: {r2:.4f}")
        print(f"    RMSE on test set: {rmse:.4f}")

        model_filename = f"{zone}_{algo}_trained_model.joblib"
        joblib.dump(model, os.path.join(output_dir, model_filename))
        logger.info(f"{zone} - {algo}: Trained model saved to {os.path.join(output_dir, model_filename)}")
        print(f"    Trained model saved to {os.path.join(output_dir, model_filename)}")

        results[zone][algo] = {"r2": r2, "rmse": rmse, "training_time": training_time, "model_path": os.path.join(output_dir, model_filename)}

# BLOC 5.E SECTION 1 - v1.2 Model Selection based on Temporal Validation

selected_models_temporal_cv = {}

for zone, algo_results in results.items():
    best_algo = None
    best_rmse = float('inf')

    for algo, metrics in algo_results.items():
        if "temporal_cv_rmse_mean" in metrics:
            rmse = metrics["temporal_cv_rmse_mean"]
            if rmse < best_rmse:
                best_rmse = rmse
                best_algo = algo

    if best_algo:
        selected_models_temporal_cv[zone] = best_algo
        logger.info(f"{zone}: Selected algorithm '{best_algo}' based on temporal CV (mean RMSE = {best_rmse:.4f}).")
        print(f"{zone}: Selected algorithm '{best_algo}' based on temporal CV (mean RMSE = {best_rmse:.4f}).")
    else:
        logger.warning(f"{zone}: No algorithm produced valid temporal CV results for selection.")
        print(f"{zone}: No algorithm produced valid temporal CV results for selection.")

# The dictionary 'selected_models_temporal_cv' now contains the name of the best algorithm for each zone


# BLOC 5.E SECTION 2 - Final Selection and Fallback

if zone in selected_models_temporal_cv:
    final_algo = selected_models_temporal_cv[zone]
    logger.info(f"{zone}: Selected algorithm from temporal CV: {final_algo}")
    print(f"  Selected algorithm from temporal CV: {final_algo}")

    # The model has already been trained during the algorithm loop.
    # We are now selecting the best one based on temporal CV results.

else:
    send_alert("warning", f"No algorithm selected via temporal CV. Using best available (R²).", zone=zone)
    print(f"  No algorithm selected via temporal CV, selecting best available (R²={best_r2_zone:.2f}).")
    final_algo, final_pred, final_r2 = best_algo_zone, best_pred_zone, best_r2_zone

    if final_algo is None:
        logger.error(f"No valid model found for zone {zone} even with best R². Applying fallback.")
        print(f"  No valid model found, applying fallback.")
        fallback = algos_to_run[0]
        logger.info(f"Fallback algorithm: {fallback}")
        print(f"  Fallback algorithm: {fallback}")
        try:
            model = None
            if fallback == "linear_regression":
                model = LinearRegression()
            elif fallback == "random_forest":
                model = RandomForestRegressor()
            elif fallback == "xgboost":
                model = xgb.XGBRegressor()
            elif fallback == "gradient_boosting":
                model = GradientBoostingRegressor()
            if model:
                model.fit(X, y)
                from sklearn.metrics import r2_score
                y_pred = model.predict(X)
                final_pred = y_pred[-1]
                final_r2 = r2_score(y, y_pred)
                final_algo = fallback
                logger.info(f"Fallback {final_algo} - {zone}: R² = {final_r2:.2f}")
                print(f"    Fallback {final_algo} - R²: {final_r2:.2f}, Prediction: {final_pred}")
            else:
                logger.error(f"Fallback algorithm '{fallback}' not recognized.")
                print(f"    Error: Fallback algorithm not recognized.")
                final_algo = "none (fallback error)"
                final_pred = None
                final_r2 = None
        except Exception as e:
            logger.error(f"Fallback error for zone {zone}: {e}")
            print(f"    Fallback error.")
            final_algo = "none (fallback error)"
            final_pred = None
            final_r2 = None

logger.info(f"Selected for {zone}: {final_algo} with R²={final_r2:.2f}, prediction={final_pred}")
print(f"  Selected for {zone}: {final_algo} (R²={final_r2:.2f}), Prediction: {final_pred}")
finalize_predictions(df.index[-1].isoformat(), zone, final_pred, None)

if bias_alert:
    print("\n--- Bias Monitoring Summary ---")
    for zone, algo_results in results.items():
        print(f"Zone: {zone}")
        for algo, metrics in algo_results.items():
            print(f"  Algorithm: {algo}, R²: {metrics['r2']:.2f}, Prediction: {metrics['prediction']}")
    print("Please review model performance and sensitive features carefully.")

# BLOC 6.A - POST-PROCESSING AND FINAL NOTIFICATION
# Clean prediction buffer and optionally notify via Telegram

def postprocess_and_notify():
    logger.info("START BLOCK 6: POST-PROCESSING AND FINAL NOTIFICATION")
    print("\n=== BLOCK 6: POST-PROCESSING AND FINAL NOTIFICATION ===")
    
    if "postprocess" not in disabled_blocks:
        logger.info("ADMIN: post-processing")
        print("Post-processing...")
        clean_predictions()
        print("Post-processing completed.")
    else:
        logger.info("ADMIN: skipping post-processing")
        print("Post-processing skipped.")

    if "notify" not in disabled_blocks:
        send_telegram_notification(f"Script completed at {datetime.datetime.now().isoformat()}")
        print("Telegram notification sent.")
    else:
        logger.info("ADMIN: skipping final notification")
        print("Telegram notification skipped.")

# BLOC 7.A - CLI PARSING AND GLOBAL SETUP
# Main entry point, CLI parsing and logger initialization

if __name__ == "__main__":
    args = parse_args()
    disabled_blocks = args.disable.split(",") if getattr(args, "disable", None) else []
    logger = setup_logging(getattr(args, "title", "default"))

    spreadsheet_ok = False
    spreadsheet = None
    legend_ws = None
    input_ws = None
    output_ws = None
    active_codes = []

    sensitive_cols = getattr(args, "sensitive_cols", None)
    if sensitive_cols:
        sensitive_cols = sensitive_cols.split(",")
        logger.info(f"Specified sensitive columns: {sensitive_cols}")
        print(f"Sensitive columns: {sensitive_cols}")

# BLOC 7.B - GOOGLE SPREADSHEET CONNECTION
# Connect to spreadsheet with retry logic

    MAX_RETRIES = 3
    RETRY_DELAY = 5

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempting spreadsheet connection ({attempt}/{MAX_RETRIES})...")
        try:
            client = get_spreadsheet_client()
            spreadsheet = client.open(SPREADSHEET_NAME)
            legend_ws = spreadsheet.worksheet(SHEET_LEGEND)
            input_ws = spreadsheet.worksheet(SHEET_INPUT)
            output_ws = spreadsheet.worksheet(SHEET_OUTPUT)
            logger.info(f"Spreadsheet connection to '{SPREADSHEET_NAME}' successful on attempt {attempt}.")
            spreadsheet_ok = True
            break
        except Exception as e:
            logger.error(f"Connection error on attempt {attempt}: {e}")
            print(f"Connection failed ({attempt}/{MAX_RETRIES}). Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    if not spreadsheet_ok:
        print(f"Unable to connect to spreadsheet '{SPREADSHEET_NAME}' after {MAX_RETRIES} attempts. Exiting.")
        sys.exit(1)

# BLOC 7.C - ACTIVE COLUMN EXTRACTION
# Retrieve and validate enabled column codes from 'legend' worksheet

    if spreadsheet_ok and legend_ws:
        print("Extracting enabled column codes from legend...")
        try:
            for row in legend_ws.get_all_records():
                code = row.get("column code")
                include = row.get("include", "NO").upper()
                if code and include == "YES":
                    active_codes.append(code)
            logger.info(f"Extracted active codes: {active_codes}")
            print(f"Active codes found: {active_codes}")

            active_codes = [str(c) for c in active_codes]
            target_map = { str(c): str(c) for c in active_codes }

        except Exception as e:
            logger.error(f"Error extracting active codes: {e}")
            print(f"Error extracting codes from legend.")
            active_codes = []
    else:
        logger.warning("Legend worksheet not accessible.")
        print("Error accessing legend. Active codes not extracted.")

# BLOC 7.D - MAIN EXECUTION ORCHESTRATOR
# Load data, run analysis, train models, handle postprocessing and notification

    if "preprocessing" not in disabled_blocks and spreadsheet_ok:
        df = load_data_and_valid(input_ws, active_codes)
        if df is not None:
            sensitive_cols = getattr(args, "sensitive_cols", None)
            sensitive_correlations, bias_detected_corr = analyze_sensitivity_correlation(df.copy(), sensitive_cols)
            shap_impact, bias_detected_shap = analyze_sensitivity_shap(df.copy(), sensitive_cols)
            bias_detected = bias_detected_corr or bias_detected_shap
            suggested_algo = analyze_speed_and_suggest_algorithm(df.copy(), bias_detected)

            algos_to_run, final_bias_alert = choose_algorithms_initial(suggested_algo, bias_detected)
            best_history = load_benchmark(spreadsheet, use_benchmark, benchmark_sheet)

            if "train" not in disabled_blocks:
                train_and_choose_modelli(df, active_codes, target_map, algos_to_run, use_benchmark, best_history, threshold_r2, cv_folds, cv_k, final_bias_alert)
            else:
                logger.info("ADMIN: skipping training")
                print("Training skipped.")

            if "postprocess" not in disabled_blocks or "notify" not in disabled_blocks:
                postprocess_and_notify()
        else:
            print("Processing stopped due to data loading errors.")
    else:
        logger.info("ADMIN: skipping data loading")
        print("Data loading skipped.")

# BLOC 7.E - FINAL TIMESTAMP
# Print completion message with timestamp

import datetime
print("\n=== Script completed ===")
print(f"Completion time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
