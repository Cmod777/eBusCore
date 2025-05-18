#!/bin/bash

# ==========================================================
# SCRIPT NAME : clean_prometheus_debug.sh
# DESCRIPTION : Rotates and cleans the debug log file.
#               Useful to prevent unlimited growth over time.
#
# AUTHOR      : Cmod777
# LICENSE     : CC BY-NC 4.0 (see LICENSE.md)
# ==========================================================

LOG_PATH="$HOME/prometheus/debug_prometheus.log"

# Keep last 500 lines of debug log
if [ -f "$LOG_PATH" ]; then
    tail -n 500 "$LOG_PATH" > "$LOG_PATH.tmp" && mv "$LOG_PATH.tmp" "$LOG_PATH"
fi
