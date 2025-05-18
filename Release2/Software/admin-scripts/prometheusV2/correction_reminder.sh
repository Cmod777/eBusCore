#!/bin/bash

# === LOAD CONFIG ===
ENV_FILE="$HOME/prometheus/.env.correction"
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "$(date) - Missing correction ENV file: $ENV_FILE" >> "/tmp/correction_env_error.log"
    exit 1
fi

# === UTILITIES ===
send_telegram() {
    local message="$1"
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="$message" > /dev/null 2>&1
    fi
}

# === TIMESTAMP CHECK ===
if [ ! -f "$LAST_CORRECTION_FILE" ]; then
    echo "$(date +%s)" > "$LAST_CORRECTION_FILE"
    echo "$(date) - Initialized timestamp" >> "$CORRECTION_LOG_FILE"
    exit 0
fi

LAST_TS=$(cat "$LAST_CORRECTION_FILE")
NOW_TS=$(date +%s)
DELTA_SEC=$((NOW_TS - LAST_TS))
DELTA_DAYS=$((DELTA_SEC / 86400))

# === TIME-BASED LOGIC ===
HOUR_NOW=$(date +%H)

if [ "$DELTA_DAYS" -ge "$CORRECTION_DAYS" ]; then
    if [ "$HOUR_NOW" -eq 10 ] || [ "$HOUR_NOW" -eq 20 ]; then
        send_telegram "Reminder: Please provide a new gas meter reading for consumption correction."
        echo "$(date) - Reminder sent (Day $DELTA_DAYS)" >> "$CORRECTION_LOG_FILE"
    fi
else
    echo "$(date) - Not yet due (Day $DELTA_DAYS)" >> "$CORRECTION_LOG_FILE"
fi
