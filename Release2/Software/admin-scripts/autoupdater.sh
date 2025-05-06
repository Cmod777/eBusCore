#!/bin/bash

# ===========================
# AUTO-UPDATER FOR DEBIAN-BASED SYSTEMS
# Author: [Your Name or Anonymous]
# Description:
#   - Automatically updates packages via apt
#   - Sends Telegram notifications
#   - Logs all activities
#   - Waits for other scripts to finish before rebooting
#   - Displays a progress bar for visual feedback
# ===========================

# Relaunch as root if not already
if [ "$EUID" -ne 0 ]; then
    exec sudo "$0" "$@"
    exit
fi

# === Configuration ===
TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"
LOG_OK="/path/to/auto_update_ok.log"
LOG_ERR="/path/to/auto_update_error.log"
LOG_UPDATES="/path/to/auto_update_list.log"
TMP_UPGR="/tmp/apt_upgrades.txt"
LOCK_FILE="/tmp/autoupdater.lock"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# === Functions ===
send_telegram() {
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$1" >/dev/null
}

log_ok() {
    echo "$TIMESTAMP - System up to date." > "$LOG_OK"
}

log_updates() {
    echo "$TIMESTAMP - Updated packages:" >> "$LOG_UPDATES"
    echo "$1" >> "$LOG_UPDATES"
}

log_error() {
    echo "$TIMESTAMP - $1" >> "$LOG_ERR"
}

wait_for_all_scripts() {
    echo "$TIMESTAMP - Waiting for all script processes to complete..." >> "$LOG_ERR"
    timeout=600  # max wait 10 minutes
    start_time=$(date +%s)
    while true; do
        if pgrep -fE "\.sh$|\.py$|\.pl$|\.rb$|\.js$|\.php$|\.lua$|\.ps1$" >/dev/null; then
            echo "$TIMESTAMP - Scripts still running..." >> "$LOG_ERR"
        else
            echo "$TIMESTAMP - No script processes detected. Proceeding." >> "$LOG_ERR"
            break
        fi
        elapsed=$(( $(date +%s) - start_time ))
        if [ "$elapsed" -ge "$timeout" ]; then
            log_error "Timeout while waiting for other scripts. Proceeding."
            send_telegram "AUTO-UPDATE WARNING: Timeout waiting for scripts. Proceeding with reboot if required."
            break
        fi
        sleep 60
    done
}

# === LOCK CHECK ===
if [ -e "$LOCK_FILE" ]; then
    echo "$TIMESTAMP - Update already in progress. Aborting." >> "$LOG_ERR"
    exit 1
fi
touch "$LOCK_FILE"

# === Progress Display ===
echo -e "\n=== AUTO-UPDATE STARTED ==="
echo "[1/4] Running apt update..."

apt update -y >> "$LOG_ERR" 2>&1
if [ $? -ne 0 ]; then
    log_error "apt update failed."
    send_telegram "AUTO-UPDATE ERROR: apt update failed. See: $LOG_ERR"
    rm -f "$LOCK_FILE"
    exit 1
fi

echo "[2/4] Checking for upgradable packages..."
apt list --upgradable 2>/dev/null | grep -v "Listing..." > "$TMP_UPGR"
if [ ! -s "$TMP_UPGR" ]; then
    log_ok
    send_telegram "AUTO-UPDATE: Nothing to update. System is up to date."
    echo "=== DONE: Nothing to update ==="
    rm -f "$TMP_UPGR" "$LOCK_FILE"
    exit 0
fi

echo "[3/4] Performing apt upgrade..."
UPDATED=$(cat "$TMP_UPGR")
apt upgrade -y >> "$LOG_ERR" 2>&1
if [ $? -ne 0 ]; then
    log_error "apt upgrade failed."
    send_telegram "AUTO-UPDATE ERROR: apt upgrade failed. See: $LOG_ERR"
    rm -f "$TMP_UPGR" "$LOCK_FILE"
    exit 1
fi

log_updates "$UPDATED"
send_telegram "AUTO-UPDATE:\nSystem updated successfully.\nPackages:\n$UPDATED"
rm -f "$TMP_UPGR"

# === Reboot Handling ===
if [ -f /var/run/reboot-required ]; then
    wait_for_all_scripts
    echo "[4/4] Reboot required. Rebooting now..."
    send_telegram "AUTO-UPDATE: Reboot required. Rebooting now."
    rm -f "$LOCK_FILE"
    reboot
else
    log_ok
    echo "[4/4] No reboot required."
    send_telegram "AUTO-UPDATE: System updated. No reboot required."
fi

rm -f "$LOCK_FILE"
echo "=== DONE: Update complete ==="
exit 0
