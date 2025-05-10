# =============================================================
#  athena.py Pipeline - notifier module
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

# === CONFIG FILE: notifier.py ===

import logging                                # Built-in logging module for log management
from notifier import send_telegram_notification  # External function to send Telegram messages


logger = logging.getLogger(__name__)          # Logger instance for this module


def send_alert(level, message, zone=None, algo=None, notify=False):
    """
    Centralized alert handler:
    - Logs the message based on severity
    - Prints it to stdout
    - Optionally sends a Telegram notification
    """

    prefix = ""                               # Prefix to contextualize the alert
    if zone:
        prefix += f"[{zone}]"
    if algo:
        prefix += f"[{algo}]"
    full_message = f"{prefix} {message}" if prefix else message

    if level == "info":                       # Info-level message (non-critical)
        logger.info(full_message)
    elif level == "warning":                  # Warning-level message (requires attention)
        logger.warning(full_message)
    elif level == "error":                    # Error-level message (critical failure)
        logger.error(full_message)
    else:
        logger.debug(full_message)            # Default fallback for undefined levels

    print(full_message)                       # Also show in CLI output

    if notify:                                # Optional Telegram alert
        send_telegram_notification(full_message)


# === INSTRUCTIONS AND SAFE USAGE ===============================================
# This module centralizes alert reporting and notification across the entire pipeline.
#
# - Use send_alert() instead of raw logger.*() or print() when reporting:
#   * Warnings (e.g. thresholds, performance drop)
#   * Errors (e.g. exceptions, training failure)
#   * Informational notices during execution
#
# - Use 'notify=True' only when real-time attention is required.
#   Avoid flooding the Telegram channel with debug or trace outputs.
#
# - You may extend this handler in the future to:
#   * Save alerts to JSON or external logs
#   * Route alerts to alternative platforms (e.g. Discord, email)
#   * Filter or suppress specific alert categories
#
# - Supported levels: "info", "warning", "error"
#   Unknown values fall back to "debug"
# ================================================================================
