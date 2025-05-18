#!/bin/bash

# ==========================================================
# SCRIPT NAME : run_prometheus.sh
# DESCRIPTION : Ensures the main Prometheus script is running.
#               Designed to be used via cron or watchdog.
#
# AUTHOR      : Cmod777
# LICENSE     : CC BY-NC 4.0+ (see LICENSE.md)
# ==========================================================

SCRIPT_PATH="$HOME/prometheus/prometheus.sh"
DEBUG_LOG="$HOME/prometheus/debug_prometheus.log"

# Check if Prometheus is already running
if pgrep -f "$SCRIPT_PATH" > /dev/null; then
    echo "$(date) - Prometheus is already running" >> "$DEBUG_LOG"
else
    echo "$(date) - Prometheus not running, restarting now" >> "$DEBUG_LOG"
    nohup bash "$SCRIPT_PATH" >> "$DEBUG_LOG" 2>&1 &
fi
