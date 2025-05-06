#!/bin/bash

# === SD Card & Script Integrity Monitor ===
# This script monitors:
# 1. SD card usage
# 2. Filesystem errors (EXT4)
# 3. File integrity of user scripts via SHA256 hashes
# It logs warnings/errors and sends Telegram alerts if needed.

# === Configuration ===
SD_THRESHOLD=90  # Percentage threshold for SD usage warning

HASH_REF_FILE="/home/username/system-scripts/.script_hashes.sha256"
HASH_TMP="/tmp/current_script_hashes.sha256"

LOG_OK="/home/username/system-scripts/sdsys_ok.log"
LOG_ERR="/home/username/system-scripts/sdsys_error.log"

TELEGRAM_TOKEN="your_telegram_bot_token"
CHAT_ID="your_chat_id"

# === Helper Functions ===
send_telegram() {
    local MESSAGE="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
         -d chat_id="${CHAT_ID}" \
         -d text="$MESSAGE" > /dev/null
}

log_ok() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - All OK. SD: ${SD_USAGE}%, No errors, hashes OK." > "$LOG_OK"
}

log_error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_ERR"
}

# === SD Card Usage Check ===
SD_USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

# === Filesystem Error Check ===
FS_ERRORS=$(dmesg | grep -iE 'ext4.*error' | tail -n 5)

# === Hash Check: Monitor Changes in .sh and .py Scripts ===
find /home -type f -name "*.sh" -o -name "*.py" -exec sha256sum {} + > "$HASH_TMP"

# Initialize hash reference if missing
if [ ! -f "$HASH_REF_FILE" ]; then
    cp "$HASH_TMP" "$HASH_REF_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Hash reference file created." >> "$LOG_OK"
fi

HASH_DIFF=$(diff "$HASH_REF_FILE" "$HASH_TMP")

# === Decision Logic ===
ERRORS=()

if (( SD_USAGE >= SD_THRESHOLD )); then
    ERRORS+=("WARNING: SD card usage at ${SD_USAGE}%")
fi

if [ -n "$FS_ERRORS" ]; then
    ERRORS+=("WARNING: Filesystem errors detected:\n$FS_ERRORS")
fi

if [ -n "$HASH_DIFF" ]; then
    ERRORS+=("WARNING: Script hash mismatch detected.")
fi

# === Reporting ===
if [ ${#ERRORS[@]} -ne 0 ]; then
    for ERR in "${ERRORS[@]}"; do
        log_error "$ERR"
    done
    send_telegram "sdsys_check ERROR(s):\n$(printf '%s\n' "${ERRORS[@]}")"
    exit 1
else
    log_ok
    exit 0
fi
