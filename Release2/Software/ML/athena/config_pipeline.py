# =============================================================
#  athena.py Pipeline - config module
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

# === CONFIG FILE: config_pipeline.py ===

# ========================
# Model performance thresholds
# ========================

THRESHOLD_R2_DEFAULT = 0.80        # Default R² threshold for model acceptance; must be between 0 and 1
CV_FOLDS_DEFAULT = 5               # Number of cross-validation folds (integer >= 2)
CV_K_DEFAULT = 1.0                 # Weighting factor for cross-validation score (float >= 0)

# ========================
# System resource thresholds
# ========================

MAX_RAM_PERCENTAGE = 75           # Maximum RAM usage allowed (%) before triggering fallback
MAX_CPU_PERCENTAGE = 80           # Maximum CPU usage allowed (%) before triggering fallback

RESOURCE_MONITORING_INTERVAL = 5  # Interval (seconds) between resource usage checks
HIGH_RESOURCE_THRESHOLD_DURATION = 10  # Seconds of sustained high usage before warning
CRITICAL_RESOURCE_THRESHOLD_DURATION = 15  # Additional seconds before auto-interruption

# ========================
# Data variability thresholds
# ========================

VELOCITY_THRESHOLD_LOW = 0.1      # Std. deviation threshold to identify low-variance features
VELOCITY_THRESHOLD_HIGH = 1.0     # Std. deviation threshold to identify highly variable features
AVG_CARDINALITY_THRESHOLD = 10    # Threshold for categorical column uniqueness (avg n. of unique values)

# ========================
# Correlation sensitivity analysis
# ========================

SENSITIVITY_CORRELATION_THRESHOLD = 0.1  # Minimum absolute correlation to flag potential bias

# ========================
# Algorithm fallback map
# ========================

LIGHTWEIGHT_ALTERNATIVES = {
    "XGBoost": ["LinearRegression", "Ridge", "GradientBoosting"],
    "GradientBoosting": ["LinearRegression", "Ridge", "RandomForest"],
    "RandomForest": ["LinearRegression", "Ridge", "GradientBoosting"],
    "LightGBM": ["LinearRegression", "Ridge", "GradientBoosting"],
    "SVR": ["LinearRegression", "Ridge", "KNN"],
    "KNN": ["LinearRegression", "Ridge"],
    "CatBoost": ["LinearRegression", "Ridge", "GradientBoosting"],
}

# Map of fallback algorithms by family. If the main model is too heavy, lighter options will be suggested.
# Do not include untested or unavailable models here.

# ========================
# SAFETY NOTE
# ========================
# Only change these constants if:
# - You fully understand the impact on resource usage and performance.
# - The change has been tested in a safe development environment.
# - You ensure compatibility with logic in the training, validation, and monitoring subsystems.
# Any misconfiguration here can cause unstable behavior or model failure.
