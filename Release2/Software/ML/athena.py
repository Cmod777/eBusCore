# === BLOCK 0: IMPORTS ===
from datetime import datetime
from cli import parse_args
# from logging_utils import setup_logging  <-- This line is commented out or removed
from auth import get_spreadsheet_client
from config import SPREADSHEET_NAME, SHEET_LEGEND, SHEET_INPUT, SHEET_OUTPUT
import sys

# Integrated ML libraries
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb

# Internal modules for data loading and training
from data_loader import load_data
from retrain import retrain_models
from output_utils import write_predictions, clean_up
from notifier import send_telegram_notification

import logging
import datetime

def setup_logging(title="default"):
    """Set up basic logging configuration."""
    log_filename = f"pipeline_{title}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def log_with_header_footer(logger, level, message, area, algo):
    timestamp = datetime.datetime.now().isoformat()
    header = f"*** START ALERT for {area} - Algorithm: {algo} - {timestamp} ***"
    footer = f"*** END ALERT for {area} - Algorithm: {algo} - {timestamp} ***"
    logger.log(level, header)
    logger.log(level, message)
    logger.log(level, footer)


# === BLOCK 1: CLI, ADMIN AND GLOBAL SETUP ===
import time  # For retry delays

# 1.1 Parse CLI arguments
args = parse_args()

# 1.2 Disabled blocks
disabled_blocks = args.disable.split(",") if getattr(args, "disable", None) else []

# 1.3 Setup logging
logger = setup_logging(getattr(args, "title", "default"))

# 1.4 Open spreadsheet and worksheets with retry
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

spreadsheet_ok = False
spreadsheet = None
legend_ws = None
input_ws = None
output_ws = None

for attempt in range(1, MAX_RETRIES + 1):
    print(f"Attempting to connect to spreadsheet (n. {attempt}/{MAX_RETRIES})...")
    try:
        client = get_spreadsheet_client()
        spreadsheet = client.open(SPREADSHEET_NAME)
        legend_ws = spreadsheet.worksheet(SHEET_LEGEND)
        input_ws = spreadsheet.worksheet(SHEET_INPUT)
        output_ws = spreadsheet.worksheet(SHEET_OUTPUT)
        logger.info(f"Connected to spreadsheet '{SPREADSHEET_NAME}' on attempt {attempt}.")
        spreadsheet_ok = True
        break  # exit loop on success
    except Exception as e:
        logger.error(f"Error on attempt {attempt}/{MAX_RETRIES}: {e}")
        print(f"Connection error (attempt {attempt}/{MAX_RETRIES}). Retrying in {RETRY_DELAY} seconds...")
        time.sleep(RETRY_DELAY)

if not spreadsheet_ok:
    print(f"Unable to connect to spreadsheet '{SPREADSHEET_NAME}' after {MAX_RETRIES} attempts. Exiting.")
    sys.exit(1)  # stop execution on failure

# 1.5 Extract active column codes from legend
active_codes = []
if spreadsheet_ok and legend_ws:
    print("Extracting active column codes from legend...")
    try:
        for row in legend_ws.get_all_records():
            code = row.get("codice colonna")
            include = row.get("includi", "NO").upper()
            if code and include == "YES":
                active_codes.append(code)
        logger.info(f"Active codes extracted from legend: {active_codes}")
        print(f"Active codes found: {active_codes}")
        print(f"Selected zones (target): {args.target.split(',') if args.target else 'all'}")
    except Exception as e:
        logger.error(f"Error extracting active codes: {e}")
        print("Error extracting active codes from legend.")
        active_codes = []
else:
    logger.warning("Cannot access legend due to spreadsheet error.")
    print("Error accessing legend. Cannot extract active codes.")

# 1.6 Validation parameters and model thresholds
use_benchmark = getattr(args, "use_benchmark", False)
benchmark_sheet = getattr(args, "benchmark_sheet", None)
threshold_r2 = getattr(args, "threshold_r2", 0.8)
cv_folds = getattr(args, "cv_folds", 5)
cv_k = getattr(args, "cv_k", 1.0)


# === BLOCK 2: DATA ANALYSIS FUNCTION AND ALGORITHM SUGGESTION ===

VELOCITY_THRESHOLD_LOW = 0.1
VELOCITY_THRESHOLD_HIGH = 1.0
VELOCITY_AVG_CARD_THRESHOLD = 10

def analyze_velocity(df):
    """
    Analyze the rate of change of features in a DataFrame
    and suggest an ML algorithm based on variability.
    """
    # compute absolute differences between consecutive samples
    diffs = df.diff().abs()

    # average velocity per feature
    avg_velocity = diffs.mean()

    # log results
    logger.info(f"Average velocity per feature: {avg_velocity.to_dict()}")

    # analyze variable types
    numeric_cols = df.select_dtypes(include='number')
    categorical_cols = df.select_dtypes(exclude='number')
    avg_std = numeric_cols.std().mean() if not numeric_cols.empty else 0
    avg_card = categorical_cols.nunique().mean() if not categorical_cols.empty else 0

    # suggest algorithm based on variability
    if not categorical_cols.empty and avg_card > VELOCITY_AVG_CARD_THRESHOLD:
        suggestion = 'random_forest'
    elif avg_std < VELOCITY_THRESHOLD_LOW:
        suggestion = 'linear_regression'
    elif avg_std > VELOCITY_THRESHOLD_HIGH:
        suggestion = 'xgboost'
    else:
        suggestion = 'gradient_boosting'

    logger.info(f"Suggested algorithm: {suggestion}")
    return suggestion

# === BLOCK 3b1: SETUP AND CORRELATION-BASED SENSITIVITY ANALYSIS ===
import pandas as pd
import numpy as np
from logging import getLogger

logger = getLogger(__name__)

def analyze_sensitivity_correlation(df, sensitive_cols=None):
    """Analyze potential feature sensitivity via correlation."""
    logger.info("START BLOCK 3b1: SENSITIVITY ANALYSIS (CORRELATION)")
    print("\n=== BLOCK 3b1: SENSITIVITY ANALYSIS (CORRELATION) ===")
    sensitive_correlations = {}
    SENSITIVITY_CORRELATION_THRESHOLD = 0.1  # configurable threshold
    bias_detected_corr = False

    if df is None or df.empty or not sensitive_cols:
        print("Warning: DataFrame empty or no sensitive columns specified for correlation.")
        return sensitive_correlations, bias_detected_corr

    feature_cols = [col for col in df.columns if col not in sensitive_cols]
    if not feature_cols:
        print("Warning: No features available for correlation analysis.")
        return sensitive_correlations, bias_detected_corr

    print("Analyzing potential feature sensitivity via correlation...")

    for sensitive_col in sensitive_cols:
        if sensitive_col in df.columns:
            sensitive_correlations[sensitive_col] = {}
            for feature_col in feature_cols:
                if pd.api.types.is_numeric_dtype(df[feature_col]) and pd.api.types.is_numeric_dtype(df[sensitive_col]):
                    corr = df[feature_col].corr(df[sensitive_col])
                    if abs(corr) > SENSITIVITY_CORRELATION_THRESHOLD:
                        bias_detected_corr = True
                        sensitive_correlations[sensitive_col].setdefault(feature_col, []).append(f"Correlation: {corr:.2f}")
                        print(f"  Sens. Col: '{sensitive_col}', Feature: '{feature_col}' - Correlation: {corr:.2f}")
                        send_telegram_notification(
                            f"**POTENTIAL BIAS (Correlation):**\n"
                            f"Significant correlation ({corr:.2f}) found between feature '{feature_col}' and sensitive column '{sensitive_col}'."
                        )

    if sensitive_correlations:
        logger.warning(f"Potential correlations between features and sensitive columns: {sensitive_correlations}")
        print(f"Warning: Potential correlations detected: {sensitive_correlations}")
    else:
        print("No significant correlations detected with specified sensitive columns.")

    return sensitive_correlations, bias_detected_corr


# === BLOCK 3b2: SHAP-BASED SENSITIVITY ANALYSIS ===
import pandas as pd
import numpy as np
import shap
from sklearn.linear_model import LinearRegression
from logging import getLogger

logger = getLogger(__name__)

def analyze_sensitivity_shap(df, sensitive_cols=None):
    """Analyze potential feature sensitivity relative to specified columns using SHAP."""
    logger.info("START BLOCK 3b2: SENSITIVITY ANALYSIS (SHAP)")
    print("\n=== BLOCK 3b2: SENSITIVITY ANALYSIS (SHAP) ===")
    shap_impact = {}
    bias_detected_shap = False
    SHAP_IMPACT_THRESHOLD = 0.05  # configurable SHAP impact threshold

    if df is None or df.empty or not sensitive_cols:
        print("Warning: DataFrame empty or no sensitive columns specified for SHAP.")
        return shap_impact, bias_detected_shap

    feature_cols = [col for col in df.columns if col not in sensitive_cols]
    if not feature_cols:
        print("Warning: No features available for SHAP analysis.")
        return shap_impact, bias_detected_shap

    print("Analyzing potential feature sensitivity with SHAP...")

    # Use a simple model for the explainer (Linear Regression)
    model = LinearRegression()
    # Sample data for the explainer for efficiency on large datasets
    explainer = shap.LinearExplainer(
        model,
        df[feature_cols].sample(n=min(100, len(df)), random_state=42),
        feature_names=feature_cols
    )

    for sensitive_col in sensitive_cols:
        if sensitive_col not in df.columns:
            print(f"Warning: Sensitive column '{sensitive_col}' not found in DataFrame.")
            continue

        shap_impact[sensitive_col] = {}

        for feature_col in feature_cols:
            if pd.api.types.is_numeric_dtype(df[feature_col]) and pd.api.types.is_numeric_dtype(df[sensitive_col]):
                try:
                    model.fit(df[[feature_col]], df[sensitive_col])
                    shap_values = explainer.shap_values(df[[feature_col]])
                    mean_abs_shap = np.mean(np.abs(shap_values))
                    shap_impact[sensitive_col][feature_col] = mean_abs_shap

                    if mean_abs_shap > SHAP_IMPACT_THRESHOLD:
                        bias_detected_shap = True
                        shap_impact[sensitive_col].setdefault(feature_col, []).append(f"Mean SHAP impact: {mean_abs_shap:.2f}")
                        print(f"  Sens. Col: '{sensitive_col}', Feature: '{feature_col}' - SHAP impact: {mean_abs_shap:.2f}")
                        send_telegram_notification(
                            f"**POTENTIAL BIAS (SHAP):**\n"
                            f"SHAP analysis indicates significant impact ({mean_abs_shap:.2f}) of feature '{feature_col}' on sensitive column '{sensitive_col}'."
                        )

                except Exception as e:
                    logger.error(f"Error during SHAP analysis for '{feature_col}' vs '{sensitive_col}': {e}")
                    print(f"  SHAP error for '{feature_col}' vs '{sensitive_col}'.")

    if shap_impact:
        logger.warning(f"Potential sensitivity impact detected via SHAP: {shap_impact}")
        print(f"Warning: Potential sensitivity impact detected via SHAP: {shap_impact}")
    else:
        print("No significant SHAP-based sensitivity impact detected.")

    return shap_impact, bias_detected_shap


# === BLOCK 3c: VELOCITY ANALYSIS AND ALGORITHM SUGGESTION ===

VELOCITY_THRESHOLD_LOW = 0.1
VELOCITY_THRESHOLD_HIGH = 1.0
VELOCITY_AVG_CARD_THRESHOLD = 10

def analyze_velocity_and_suggest(df, bias_detected=False):
    """
    Analyze pattern velocity and suggest an algorithm,
    also considering potential bias.
    """
    logger.info("START BLOCK 3c: VELOCITY ANALYSIS AND ALGORITHM SUGGESTION")
    print("\n=== BLOCK 3c: VELOCITY ANALYSIS AND ALGORITHM SUGGESTION ===")
    suggested_algo = getattr(args, "algorithm", None)
    if "analysis" not in disabled_blocks and getattr(args, "analisi_velocita", "no") == "si" and df is not None:
        logger.info("ADMIN: velocity analysis and algorithm suggestion")
        print("Analyzing pattern velocity to suggest algorithm...")
        diffs = df.diff().abs()
        avg_velocity = diffs.mean()
        logger.info(f"Average velocity per feature: {avg_velocity.to_dict()}")

        numeric_cols = df.select_dtypes(include='number')
        categorical_cols = df.select_dtypes(exclude='number')
        avg_std = numeric_cols.std().mean() if not numeric_cols.empty else 0
        avg_card = categorical_cols.nunique().mean() if not categorical_cols.empty else 0

        if not categorical_cols.empty and avg_card > VELOCITY_AVG_CARD_THRESHOLD:
            suggestion = 'random_forest'
        elif avg_std < VELOCITY_THRESHOLD_LOW:
            suggestion = 'linear_regression'
        elif avg_std > VELOCITY_THRESHOLD_HIGH:
            suggestion = 'xgboost'
        else:
            suggestion = 'gradient_boosting'
        suggested_algo = suggestion
        print(f"Suggested algorithm: {suggested_algo}")

        if bias_detected:
            print("Warning: potential bias detected. Consider alternative algorithms.")

    else:
        logger.info(f"ADMIN: skip velocity analysis, using default algorithm: {suggested_algo}")
        print(f"Velocity analysis skipped. Using default algorithm: {suggested_algo}")
        if bias_detected:
            print("Warning: potential bias detected. Consider alternative algorithms.")

    return suggested_algo


# === BLOCK 4a1: INITIAL BIAS ALERT HANDLING ===
def handle_bias_alert(suggested_algo, bias_detected):
    """Handle potential bias alert."""
    bias_alert = bias_detected
    algos_to_run = [suggested_algo]

    if bias_alert:
        print("\nALERT: Potential bias detected in model (via correlation or SHAP).")
        print(f"Suggested algorithm is: {suggested_algo}")
        print("Consider using different algorithms to mitigate potential bias.")
    else:
        print(f"Recommended algorithm: {suggested_algo}")

    return bias_alert, algos_to_run


# === BLOCK 4a2: MANUAL OR AUTOMATIC ALGORITHM SELECTION ===
def choose_algorithms(suggested_algo, bias_alert, algos_to_run):
    """Allow manual or automatic selection of algorithms."""
    if bias_alert:
        if sys.stdin.isatty():
            ask_more = input("Do you want to manually choose algorithms to run? [Y/n]: ")
            if ask_more.lower() in ["", "y", "yes"]:
                choices = ["linear_regression", "random_forest", "xgboost", "gradient_boosting", "all"]
                print("Choose algorithm:")
                for i, opt in enumerate(choices, 1):
                    print(f" [{i}] {opt}")
                selected = input("Select numbers of desired algorithms (comma-separated, or 'all'): ")
                if selected.lower() == "all":
                    algos_to_run = choices[:-1]
                else:
                    algos_to_run = []
                    for s in selected.split(","):
                        s = s.strip()
                        if s.isdigit() and 1 <= int(s) <= len(choices):
                            idx = int(s) - 1
                            if idx < len(choices)-1:
                                algos_to_run.append(choices[idx])
                            else:
                                algos_to_run = choices[:-1]
                                break
                        else:
                            print(f"Invalid selection: {s}")
                    if not algos_to_run:
                        algos_to_run = [suggested_algo]
                        print(f"No valid selection, using suggested: {suggested_algo}")
            else:
                # non-interactive fallback adds an alternative algorithm
                alt = {"linear_regression":"random_forest","random_forest":"linear_regression",
                       "xgboost":"gradient_boosting","gradient_boosting":"xgboost"}
                algos_to_run.append(alt.get(suggested_algo, suggested_algo))
                algos_to_run = list(set(algos_to_run))
                print(f"Automatically added alternative algorithm: {algos_to_run[1]}")
        else:
            alt = {"linear_regression":"random_forest","random_forest":"linear_regression",
                   "xgboost":"gradient_boosting","gradient_boosting":"xgboost"}
            algos_to_run.append(alt.get(suggested_algo, suggested_algo))
            algos_to_run = list(set(algos_to_run))
            print(f"Non-interactive mode: bias detected, running: {algos_to_run}")
    elif sys.stdin.isatty():
        use_default = input("Use the suggested algorithm? [Y/n]: ")
        if use_default.lower() not in ["", "y", "yes"]:
            choices = ["linear_regression","random_forest","xgboost","gradient_boosting","all"]
            print("Choose algorithm:")
            for i, opt in enumerate(choices,1):
                print(f" [{i}] {opt}")
            sel = input("Select number: ")
            if sel.isdigit():
                idx = int(sel)-1
                if idx == 4:
                    algos_to_run = choices[:-1]
                elif 0 <= idx < 4:
                    algos_to_run = [choices[idx]]
                else:
                    print(f"Invalid, using suggested: {suggested_algo}")
            else:
                print(f"Invalid input, using suggested: {suggested_algo}")
    else:
        algos_to_run = [suggested_algo]
        print(f"Non-interactive mode, using: {suggested_algo}")

    return algos_to_run, bias_alert


# === BLOCK 4a3: INITIAL ALGORITHM SELECTION ===
def initial_algorithm_selection(suggested_algo, bias_detected):
    bias_alert, initial_list = handle_bias_alert(suggested_algo, bias_detected)
    final_list, final_alert = choose_algorithms(suggested_algo, bias_alert, initial_list)
    return final_list, final_alert

# === BLOCK 4b: BENCHMARK LOADING ===
def load_benchmark(spreadsheet, use_benchmark, benchmark_sheet):
    """Load historical benchmark values if requested."""
    best_history = {}
    if use_benchmark and benchmark_sheet and spreadsheet:
        ws_bench = spreadsheet.worksheet(benchmark_sheet)
        print("Loading benchmark history...")
        for rec in ws_bench.get("A1:Z"):  # get all rows as lists
            if rec and len(rec) >= 2 and rec[0] is not None and rec[1] is not None:
                try:
                    # assume rec[0]=zone, rec[1]=best_r2
                    best_history[rec[0]] = float(rec[1])
                except ValueError:
                    logger.warning(f"Invalid R² value in benchmark for zone '{rec[0]}': '{rec[1]}'. Ignored.")
                    print(f"Warning: Invalid R² value for zone '{rec[0]}'.")
            elif rec:
                logger.warning(f"Incomplete or invalid benchmark row: {rec}")
                print("Warning: Incomplete or invalid benchmark row.")
        print("Benchmark history loaded.")
    elif use_benchmark and not benchmark_sheet:
        print("Warning: use_benchmark is active but no benchmark_sheet specified.")
        logger.warning("use_benchmark active but no benchmark_sheet specified.")
    elif benchmark_sheet and not use_benchmark:
        print("Warning: benchmark_sheet specified but use_benchmark not active.")
        logger.warning("benchmark_sheet specified but use_benchmark not active.")
    return best_history


# === BLOCK 4c: EMPTY PLACEHOLDER FOR FUTURE EXTENSIONS ===
# This block is intentionally left empty for future logic additions.
pass


# === BLOCK 5a: SETUP AND ZONE ITERATION ===
from tqdm import tqdm

def train_and_evaluate_models(df, active_codes, target_map, algos_to_run,
                              use_benchmark, best_history,
                              threshold_r2, cv_folds, cv_k, bias_alert=False):
    """Train and evaluate models for each zone."""
    logger.info("START BLOCK 5: TRAINING AND EVALUATION")
    print("\n=== BLOCK 5: TRAINING AND EVALUATION ===")
    if df is None:
        logger.warning("DataFrame not loaded. Cannot train.")
        print("Warning: DataFrame not loaded. Cannot train.")
        return

    zones = args.target.split(",") if getattr(args, "target", None) else list(target_map.keys())
    if not zones:
        logger.warning("No zones specified for training.")
        print("Warning: No zones specified for training.")
        return

    if bias_alert:
        print("WARNING: Potential bias detected. Model results will be monitored carefully.")

    print("Starting training and evaluation:")
    results = {}

    for zone in tqdm(zones, desc="Zone Progress"):
        logger.info(f"--- ZONE: {zone} ---")
        print(f"\n--- ZONE: {zone} ---")
        if zone not in target_map:
            logger.error(f"Zone '{zone}' not in target_map. Skipping.")
            print(f"Error: Zone '{zone}' not in target_map.")
            continue

        target_col = target_map[zone]
        feature_cols = [c for c in active_codes if c != target_col]

        if not feature_cols:
            logger.warning(f"No features available for zone '{zone}'. Skipping.")
            print(f"Warning: No features available for zone '{zone}'.")
            continue

        X = df[feature_cols]
        y = df[target_col]
        results[zone] = {}
        final_algo = None
        final_pred = None
        final_r2 = None
        best_r2_zone = -float('inf')
        best_algo_zone = None
        best_pred_zone = None

        # actual training per algorithm happens in BLOCKs 5b and 5c
        pass


# === BLOCK 5b1: BASE TRAINING AND EVALUATION ===
def train_and_evaluate(algo, model, X, y, zone, logger,
                       threshold_r2, effective_thr,
                       best_r2_zone, best_algo_zone, best_pred_zone, results):
    """
    Fit model, compute R², record alerts if below threshold,
    and update best-per-zone tracking.
    """
    from sklearn.metrics import r2_score

    r2 = -float('inf')
    y_pred = None
    alerts = []

    try:
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        logger.info(f"{zone} [{algo}]: R² = {r2:.2f}")
        print(f"    R² on full dataset: {r2:.2f}")
        results[zone].setdefault(algo, {})["r2"] = r2
        results[zone].setdefault(algo, {})["prediction"] = y_pred[-1]

        if r2 < threshold_r2:
            msg = f"**WARNING:** Performance below threshold (R²={r2:.2f} < {threshold_r2:.2f})"
            logger.warning(f"{zone} [{algo}]: {msg}")
            print(f"    {msg}")
            alerts.append(msg)

        if r2 > best_r2_zone:
            best_r2_zone = r2
            best_algo_zone = algo
            best_pred_zone = y_pred[-1]

    except Exception as e:
        logger.error(f"Error training/evaluating {algo} on zone {zone}: {e}")
        print("    Error during training/evaluation.")
        alerts.append(f"Error during training/evaluation: {e}")

    if alerts:
        results[zone].setdefault(algo, {})["alerts"] = alerts

    return r2, y_pred, best_r2_zone, best_algo_zone, best_pred_zone


# === BLOCK 5b2.1: FEATURE IMPORTANCE AND SHAP CALCULATION ===
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

def compute_shap_feature_importance(algo, model, X, zone, logger, r2, threshold_r2):
    """
    Compute intrinsic feature importance (if available) and SHAP values,
    save SHAP summary plot if performance is good.
    """
    feature_importance_shap = None
    shap_values = None

    try:
        # intrinsic importance
        if algo in ["random_forest", "xgboost", "gradient_boosting"] and hasattr(model, "feature_importances_"):
            imp = pd.DataFrame(
                zip(X.columns, model.feature_importances_),
                columns=["Feature", "Importance"]
            ).sort_values("Importance", ascending=False)
            logger.info(f"{zone} - {algo} Feature Importance:\n{imp.head().to_string()}")
            print(f"    {algo} Feature Importance:\n{imp.head()}")

        # SHAP values
        explainer = shap.Explainer(model, X)
        shap_values = explainer(X)
        mean_abs = np.abs(shap_values.values).mean(axis=0)
        feature_importance_shap = pd.DataFrame(
            zip(X.columns, mean_abs),
            columns=["Feature", "SHAP Importance"]
        ).sort_values("SHAP Importance", ascending=False)
        logger.info(f"{zone} - {algo} SHAP Importance:\n{feature_importance_shap.head().to_string()}")
        print(f"    {algo} SHAP Importance:\n{feature_importance_shap.head()}")

        if r2 > threshold_r2 - 0.05:
            shap.summary_plot(shap_values, features=X, show=False)
            plt.title(f"{zone} - SHAP Summary Plot ({algo})")
            plt.savefig(f"shap_summary_{zone}_{algo}.png")
            plt.close()
            logger.info(f"{zone} - SHAP summary plot saved.")
            print(f"  {zone} - SHAP summary plot generated.")

    except Exception as e:
        logger.error(f"Error computing SHAP/importance for {algo} on zone {zone}: {e}")
        print("  Error computing SHAP or feature importance.")

    return feature_importance_shap, shap_values


# === BLOCK 5b2.2: BIAS ANALYSIS ===
def analyze_bias(algo, X, zone, logger, feature_importance_shap, shap_values, bias_detected_corr, results):
    """
    Perform deeper bias analysis: compare SHAP impact for top features
    across median-split groups, fallback to correlation warning if needed.
    """
    bias_success = False
    alerts = results.setdefault(zone, {}).setdefault(algo, {}).setdefault("alerts", [])

    if X is not None and feature_importance_shap is not None and shap_values is not None:
        try:
            top_features = feature_importance_shap["Feature"].head(3).tolist()
            for feat in top_features:
                med = X[feat].median()
                low_grp = X[X[feat] <= med]
                high_grp = X[X[feat] > med]
                if not low_grp.empty and not high_grp.empty:
                    shap_low = shap_values[low_grp.index].values[:, X.columns.get_loc(feat)].mean()
                    shap_high = shap_values[high_grp.index].values[:, X.columns.get_loc(feat)].mean()
                    diff = abs(shap_high - shap_low)
                    if diff > 0.05:
                        msg = f"**POTENTIAL BIAS:** Difference in impact of '{feat}' between groups (diff={diff:.4f})"
                        logger.warning(f"{zone} [{algo}]: {msg}")
                        print(f"    {msg}")
                        alerts.append(msg)
                        bias_success = True
                        break
        except Exception as e:
            msg = f"Error in soft bias analysis: {e}"
            logger.warning(f"{zone} [{algo}]: {msg}")
            print(f"    {msg}")
            alerts.append(msg)

    if not bias_success:
        logger.info(f"{zone} [{algo}]: Soft bias analysis did not detect issues; fallback.")
        print("  Deep bias analysis did not detect issues.")
        if bias_detected_corr:
            msg = "**POTENTIAL BIAS (correlation):** Check features correlated with sensitive variables."
            logger.warning(f"{zone} [{algo}]: {msg}")
            print(f"    {msg}")
            alerts.append(msg)

    if alerts:
        results[zone][algo]["alerts"] = alerts

  # === BLOCK 5b3: TRAINING AND EVALUATION PER ALGORITHM ===
        for algo in algos_to_run:
            logger.info(f"Trying algorithm: {algo}")
            print(f"  Trying algorithm: {algo}")
            model = None
            if algo == "linear_regression":
                model = LinearRegression()
            elif algo == "random_forest":
                model = RandomForestRegressor()
            elif algo == "xgboost":
                model = xgb.XGBRegressor()
            elif algo == "gradient_boosting":
                model = GradientBoostingRegressor()
            else:
                logger.warning(f"Algorithm '{algo}' not recognized. Skipping.")
                print(f"  Warning: Algorithm '{algo}' not recognized.")
                continue

            # dynamic threshold via cross‑validation
            from sklearn.model_selection import cross_val_score
            thr_cv = -float('inf')
            try:
                cv_scores = cross_val_score(model, X, y, cv=cv_folds, scoring="r2")
                thr_cv = cv_scores.mean() - cv_k * cv_scores.std()
                logger.info(f"{zone} - {algo}: CV mean R² = {cv_scores.mean():.2f}, std = {cv_scores.std():.2f}, CV threshold = {thr_cv:.2f}")
                print(f"    CV mean R²: {cv_scores.mean():.2f}, CV threshold: {thr_cv:.2f}")
            except Exception as e:
                logger.error(f"Error during cross-validation for {algo} in zone {zone}: {e}")
                print(f"    Error during cross-validation.")

            hist_thr = best_history.get(zone, 0) if use_benchmark else 0
            thr_eff = max(hist_thr, thr_cv, threshold_r2)
            logger.info(f"Effective R² threshold for {algo} in {zone}: {thr_eff:.2f}")
            print(f"    Effective R² threshold: {thr_eff:.2f}")

            # call BLOCK 5b1 (training and evaluation)
            r2, y_pred, best_r2_zone, best_algo_zone, best_pred_zone = train_and_evaluate(
                algo, model, X, y, zone, logger,
                threshold_r2, thr_eff,
                best_r2_zone, best_algo_zone, best_pred_zone,
                results
            )

            # call BLOCK 5b2.1 (feature importance & SHAP)
            feature_importance_shap, shap_values = compute_shap_feature_importance(
                algo, model, X, zone, logger, r2, threshold_r2
            )

            # call BLOCK 5b2.2 (bias analysis)
            analyze_bias(
                algo, X, zone, logger,
                feature_importance_shap, shap_values,
                bias_detected_corr, results
            )

            # log and print any alerts for this algorithm and zone
            if zone in results and algo in results[zone] and "alerts" in results[zone][algo]:
                print(f"\n  *** ALERT for {zone} - Algorithm: {algo} ***")
                all_alerts = ""
                for alert in results[zone][algo]["alerts"]:
                    print(f"    - {alert}")
                    all_alerts += f"- {alert}\n"
                print("  *****************************************\n")

                log_with_header_footer(
                    logger, logging.WARNING,
                    f"Alerts detected:\n{all_alerts.rstrip()}",
                    zone, algo
                )

            # if performance above threshold, allow user to accept final
            if r2 >= thr_eff and sys.stdin.isatty():
                confirm = input(
                    f"  {algo} exceeds threshold (R²={r2:.2f} ≥ {thr_eff:.2f}). "
                    f"Accept this as final for {zone}? [Y/n]: "
                )
                if confirm.lower() in ["", "y", "yes"]:
                    final_algo, final_pred, final_r2 = algo, y_pred[-1], r2
                    break
            elif final_algo is None and r2 >= thr_eff:
                final_algo, final_pred, final_r2 = algo, y_pred[-1], r2


# === BLOCK 5c: FINAL SELECTION AND FALLBACK ===
        if final_algo is None:
            logger.warning(f"No model exceeded threshold for zone {zone}. Using best-performing model.")
            print(f"  No model exceeded threshold; selected {best_algo_zone} (R²={best_r2_zone:.2f}).")
            final_algo, final_pred, final_r2 = best_algo_zone, best_pred_zone, best_r2_zone

            if final_algo is None:
                logger.error(f"No valid model found for zone {zone}. Falling back.")
                print("  No valid model found; falling back.")
                fallback = algos_to_run[0]
                logger.info(f"Fallback algorithm: {fallback}")
                print(f"  Fallback algorithm: {fallback}")
                try:
                    if fallback == "linear_regression":
                        model = LinearRegression()
                    elif fallback == "random_forest":
                        model = RandomForestRegressor()
                    elif fallback == "xgboost":
                        model = xgb.XGBRegressor()
                    elif fallback == "gradient_boosting":
                        model = GradientBoostingRegressor()
                    else:
                        model = None

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
                        raise ValueError(f"Unknown fallback algorithm '{fallback}'")
                except Exception as e:
                    logger.error(f"Error during fallback for zone {zone}: {e}")
                    print("    Error during fallback.")
                    final_algo = None
                    final_pred = None
                    final_r2 = None

        logger.info(f"Selected for {zone}: {final_algo} with R²={final_r2:.2f}, prediction={final_pred}")
        print(f"  Selected for {zone}: {final_algo} (R²={final_r2:.2f}), Prediction: {final_pred}")
        scrivi_previsioni_preml2(df.index[-1].isoformat(), zone, final_pred, None)

    if bias_alert:
        print("\n--- Bias Monitoring Summary ---")
        for zone, algos in results.items():
            print(f"Zone: {zone}")
            for algo, metrics in algos.items():
                print(f"  Algorithm: {algo}, R²: {metrics['r2']:.2f}, Prediction: {metrics['prediction']}")
        print("Recommended to carefully review model performance relative to sensitive columns.")


# === BLOCK 6: POST-PROCESSING AND FINAL NOTIFICATION ===
def post_process_and_notify():
    """Perform post-processing and send final notification."""
    logger.info("START BLOCK 6: POST-PROCESSING AND FINAL NOTIFICATION")
    print("\n=== BLOCK 6: POST-PROCESSING AND FINAL NOTIFICATION ===")
    if "postprocess" not in disabled_blocks:
        logger.info("ADMIN: post-processing")
        print("Post-processing...")
        pulisci_preml2()
        print("Post-processing completed.")
    else:
        logger.info("ADMIN: skip post-processing")
        print("Post-processing skipped.")

    if "notify" not in disabled_blocks:
        send_telegram_notification(f"Script completed at {datetime.datetime.now().isoformat()}")
        print("Telegram notification sent.")
    else:
        logger.info("ADMIN: skip final notification")
        print("Telegram notification skipped.")

  # === BLOCK 7a: INITIAL SETUP ===
if __name__ == "__main__":
    args = parse_args()
    disabled_blocks = args.disable.split(",") if getattr(args, "disable", None) else []
    logger = setup_logging(getattr(args, "title", "default"))

    # spreadsheet and worksheet placeholders
    spreadsheet_ok = False
    spreadsheet = None
    legend_ws = None
    input_ws = None
    output_ws = None
    active_codes = []

    sensitive_cols = getattr(args, "sensitive_cols", None)
    if sensitive_cols:
        sensitive_cols = sensitive_cols.split(",")
        logger.info(f"Sensitive columns specified: {sensitive_cols}")
        print(f"Sensitive columns specified: {sensitive_cols}")

# === BLOCK 7b: SPREADSHEET CONNECTION HANDLING ===
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempting to connect to spreadsheet (attempt {attempt}/{MAX_RETRIES})...")
        try:
            client = get_spreadsheet_client()
            spreadsheet = client.open(SPREADSHEET_NAME)
            legend_ws = spreadsheet.worksheet(SHEET_LEGENDA)
            input_ws = spreadsheet.worksheet(SHEET_INPUT)
            output_ws = spreadsheet.worksheet(SHEET_OUTPUT)
            logger.info(f"Connected to spreadsheet '{SPREADSHEET_NAME}' on attempt {attempt}.")
            spreadsheet_ok = True
            break
        except Exception as e:
            logger.error(f"Error on attempt {attempt}/{MAX_RETRIES} connecting: {e}")
            print(f"Connection error (attempt {attempt}/{MAX_RETRIES}). Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    if not spreadsheet_ok:
        print(f"Unable to connect to spreadsheet '{SPREADSHEET_NAME}' after {MAX_RETRIES} attempts. Exiting.")
        sys.exit(1)

# === BLOCK 7c: EXTRACT ACTIVE CODES ===
    if spreadsheet_ok and legend_ws:
        print("Extracting active column codes from legend...")
        try:
            for row in legend_ws.get_all_records():
                code = row.get("codice colonna")
                include = row.get("includi", "NO").upper()
                if code and include == "YES":
                    active_codes.append(code)
            logger.info(f"Active codes extracted from legend: {active_codes}")
            print(f"Active codes found: {active_codes}")

            # convert codes (ints) to strings to match DataFrame column names
            active_codes = [str(c) for c in active_codes]

            # dynamic target_map: all possible columns, though not all will be used
            target_map = {str(c): str(c) for c in active_codes}

        except Exception as e:
            logger.error(f"Error extracting active codes: {e}")
            print("Error extracting active codes from legend.")
            active_codes = []
    else:
        logger.warning("Cannot access legend due to spreadsheet error.")
        print("Error accessing legend. Cannot extract active codes.")

# === BLOCK 7d: RUN MAIN BLOCKS ===
    if "preprocessing" not in disabled_blocks and spreadsheet_ok:
        df = load_and_validate_data(input_ws, active_codes)
        if df is not None:
            sensitive_cols = getattr(args, "sensitive_cols", None)
            corr_impact, bias_corr = analyze_sensitivity_correlation(df.copy(), sensitive_cols)
            shap_impact, bias_shap = analyze_sensitivity_shap(df.copy(), sensitive_cols)
            bias_detected = bias_corr or bias_shap
            suggested_algo = analyze_speed_and_suggest(df.copy(), bias_detected)

            # BLOCK 4: algorithm choice & benchmark loading
            algos_to_run, final_bias_alert = choose_initial_algorithms(suggested_algo, bias_detected)
            best_history = load_benchmark(spreadsheet, use_benchmark, benchmark_sheet)

            # BLOCK 5: training and evaluation
            if "train" not in disabled_blocks:
                train_and_evaluate_models(
                    df, active_codes, target_map,
                    algos_to_run, use_benchmark, best_history,
                    threshold_r2, cv_folds, cv_k, final_bias_alert
                )
            else:
                logger.info("ADMIN: skip train/predict")
                print("Training and prediction skipped.")

            # BLOCK 6: post-processing & notification
            if "postprocess" not in disabled_blocks or "notify" not in disabled_blocks:
                post_process_and_notify()
        else:
            print("Processing aborted due to data loading errors.")
    else:
        logger.info("ADMIN: skip data loading")
        print("Data loading skipped.")

import datetime
print("\n=== Script completed ===")
print(f"Completion time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ----------------------------------------------------------------------------
    # DISCLAIMER: This software is subject to license. See LICENSE or LICENSE.md
    #             for full terms and conditions.
    # ----------------------------------------------------------------------------
