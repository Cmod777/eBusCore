#!/bin/bash

# === GAS CONSUMPTION CORRECTION SCRIPT ===
# This script helps calibrate Prometheus gas estimation against real meter readings.
# It supports interactive input, comparison of V1 and V2 logs, error calculation,
# and auto-adjustment of the correction percentage for V2.

CORRECTION_ENV="$HOME/prometheus/.env.correction"
PROMETHEUS_V1_LOG="$HOME/prometheus/prometheus_success.log"
PROMETHEUS_V2_LOG="$HOME/prometheus/prometheus_success_v2.log"
V2_ENV_FILE="$HOME/prometheus/.env.prometheus"

TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

# --- Telegram notification ---
send_telegram() {
    local msg="$1"
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d text="$msg" > /dev/null
}

# --- Helper for numeric check ---
is_number() {
    [[ "$1" =~ ^[0-9]+([.][0-9]+)?$ ]]
}

# --- Prompt for gas reading and timestamp ---
prompt_gas_reading() {
    local index="$1"
    local reading date

    echo "== ${index^^} GAS READING =="

    read -p "Enter gas reading (e.g. 1755.930): " reading
    if ! is_number "$reading"; then
        echo "[ERROR] Invalid number format."
        exit 1
    fi

    read -p "Enter date and time (e.g. 2025-05-18 12:05): " date
    if ! date -d "$date" "+%s" >/dev/null 2>&1; then
        echo "[ERROR] Invalid date/time format."
        exit 1
    fi

    echo "$reading;$date" > "$CORRECTION_ENV.tmp.$index"
    echo "[OK] Reading saved: $reading m³ at $date"
}

# --- Load readings ---
load_readings() {
    if [ ! -f "$CORRECTION_ENV.tmp.first" ] || [ ! -f "$CORRECTION_ENV.tmp.second" ]; then
        return 1
    fi
    FIRST_READING=$(cut -d';' -f1 "$CORRECTION_ENV.tmp.first")
    FIRST_TIMESTAMP=$(date -d "$(cut -d';' -f2 "$CORRECTION_ENV.tmp.first")" +%s)
    SECOND_READING=$(cut -d';' -f1 "$CORRECTION_ENV.tmp.second")
    SECOND_TIMESTAMP=$(date -d "$(cut -d';' -f2 "$CORRECTION_ENV.tmp.second")" +%s)
}

# --- Sum Prometheus gas usage from logs ---
sum_gas_from_log() {
    local log_file="$1"
    awk -v start="$FIRST_TIMESTAMP" -v end="$SECOND_TIMESTAMP" '
    $0 ~ /"timestamp_start"/ {
        match($0, /timestamp_start": "([^"]+)/, a)
        cmd = "date -d \"" a[1] "\" +%s"
        cmd | getline ts
        close(cmd)
        if (ts >= start && ts <= end) {
            match($0, /"gas_consumed": "([0-9.]+)/, g)
            sum += g[1]
        }
    }
    END { printf("%.6f\n", sum) }
    ' "$log_file"
}

# --- Compute correction percentage ---
calculate_percentage_error() {
    local predicted="$1"
    local real="$2"
    if (( $(echo "$real == 0" | bc -l) )); then
        echo "100"
    else
        echo "scale=4; (100 * ($predicted - $real) / $real)" | bc
    fi
}

# === MAIN LOGIC ===

if [ ! -f "$CORRECTION_ENV.tmp.first" ]; then
    prompt_gas_reading "first"
    echo "[!] Wait 7 days before entering the second reading."
    exit 0
fi

if [ ! -f "$CORRECTION_ENV.tmp.second" ]; then
    prompt_gas_reading "second"
fi

load_readings

if (( "$SECOND_TIMESTAMP" <= "$FIRST_TIMESTAMP" )); then
    echo "[ERROR] Second reading must be after the first."
    exit 1
fi

GAS_REAL=$(echo "scale=6; $SECOND_READING - $FIRST_READING" | bc)
GAS_V1=$(sum_gas_from_log "$PROMETHEUS_V1_LOG")
GAS_V2=$(sum_gas_from_log "$PROMETHEUS_V2_LOG")

ERROR_V1=$(calculate_percentage_error "$GAS_V1" "$GAS_REAL")
ERROR_V2=$(calculate_percentage_error "$GAS_V2" "$GAS_REAL")

CURRENT_CORRECTION=$(grep -E "^CORRECTION_PERCENTAGE=" "$V2_ENV_FILE" | cut -d= -f2)
NEW_CORRECTION=$(echo "scale=4; $CURRENT_CORRECTION - $ERROR_V2" | bc)

NEW_PRECISION=$(echo "scale=2; 100 - sqrt(($ERROR_V2)^2)" | bc)

echo ""
echo "=== SUMMARY ==="
echo "Period: $(date -d @$FIRST_TIMESTAMP) → $(date -d @$SECOND_TIMESTAMP)"
echo "Real reading delta:  $GAS_REAL m³"
echo "Prometheus V1:       $GAS_V1 m³ (error ≈ $ERROR_V1%)"
echo "Prometheus V2:       $GAS_V2 m³ (error ≈ $ERROR_V2%)"
echo ""
echo "Current correction V2:  +$CURRENT_CORRECTION%"
echo "Suggested correction:   +$NEW_CORRECTION%"
echo "Previous precision:     ~$(echo "scale=0; 100 - $ERROR_V2" | bc)%"
echo "Predicted new precision:~$NEW_PRECISION%"
echo ""

read -p "Apply suggested correction? [y/N]: " apply
if [[ "$apply" =~ ^[Yy]$ ]]; then
    sed -i "s/^CORRECTION_PERCENTAGE=.*/CORRECTION_PERCENTAGE=$NEW_CORRECTION/" "$V2_ENV_FILE"
    echo "[OK] Correction updated in: $V2_ENV_FILE"
else
    echo "[!] Correction NOT applied."
fi

send_telegram "Correction analysis done. Real usage: $GAS_REAL m³. V1: $GAS_V1 m³, V2: $GAS_V2 m³. Suggested correction: +$NEW_CORRECTION%."

# Cleanup temp files
rm -f "$CORRECTION_ENV.tmp.first" "$CORRECTION_ENV.tmp.second"
