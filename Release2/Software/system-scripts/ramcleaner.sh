#!/bin/bash

# =============================================
# Script: ramcleaner.sh
# Purpose: Monitor RAM and SWAP usage, log status, notify via Telegram,
# and optionally trigger a system reboot under extreme memory pressure.
# =============================================

# --- Configuration ---
RAM_THRESHOLD_WARN=80      # Warning threshold for RAM (%)
RAM_THRESHOLD_CRIT=95      # Critical threshold for RAM (%)
SWAP_THRESHOLD_CRIT=90     # Critical threshold for SWAP (%)

LOG_OK="/home/pi/system-scripts/ramcleaner_ok.log"
LOG_ERR="/home/pi/system-scripts/ramcleaner_error.log"
TMP_TOP="/tmp/ram_top_processes.txt"

TELEGRAM_TOKEN="your_telegram_bot_token"
CHAT_ID="your_telegram_chat_id"

# --- Timestamp for logs ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# --- Function to send Telegram notification ---
send_telegram() {
    local MESSAGE="$1"
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MESSAGE" >/dev/null
}

# --- Logging helpers ---
log_ok() {
    echo "$TIMESTAMP - All OK. RAM: ${RAM_USED}%, SWAP: ${SWAP_USED}%." > "$LOG_OK"
}

log_error() {
    echo "$TIMESTAMP - $1" >> "$LOG_ERR"
}

# --- RAM + SWAP Monitoring ---
MEM_TOTAL=$(free -m | awk '/^Mem:/ {print $2}')
MEM_USED=$(free -m | awk '/^Mem:/ {print $3}')
RAM_USED=$(( 100 * MEM_USED / MEM_TOTAL ))

SWAP_TOTAL=$(free -m | awk '/^Swap:/ {print $2}')
SWAP_USED_RAW=$(free -m | awk '/^Swap:/ {print $3}')
SWAP_USED=0
if [ "$SWAP_TOTAL" -gt 0 ]; then
    SWAP_USED=$(( 100 * SWAP_USED_RAW / SWAP_TOTAL ))
fi

# --- Warning / Critical Conditions ---
if (( RAM_USED >= RAM_THRESHOLD_CRIT && SWAP_USED >= SWAP_THRESHOLD_CRIT )); then
    log_error "CRITICAL: RAM ${RAM_USED}% + SWAP ${SWAP_USED}%"
    ps -eo pid,user,comm,%mem --sort=-%mem | head -n 20 > "$TMP_TOP"
    cat "$TMP_TOP" >> "$LOG_ERR"

    send_telegram "CRITICAL: RAM ${RAM_USED}%, SWAP ${SWAP_USED}%.\nTop RAM users:\n$(cat $TMP_TOP)"

    # Optional: Reboot if system is critically overloaded
    # reboot

    rm -f "$TMP_TOP"
    exit 1
elif (( RAM_USED >= RAM_THRESHOLD_WARN )); then
    log_error "WARNING: RAM usage high at ${RAM_USED}%"
    ps -eo pid,user,comm,%mem --sort=-%mem | head -n 10 > "$TMP_TOP"
    cat "$TMP_TOP" >> "$LOG_ERR"

    send_telegram "WARNING: RAM usage at ${RAM_USED}%.\nTop RAM users:\n$(cat $TMP_TOP)"
    rm -f "$TMP_TOP"
    exit 0
fi

# --- All OK ---
log_ok
rm -f "$TMP_TOP"
exit 0
