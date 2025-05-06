#!/bin/bash

# ================================
# CPU Cooler Control Script
# For Raspberry Pi with Shelly relay
# Author: [REDACTED]
# Description: Monitors CPU temp and controls ventilation via Shelly
# Dependencies: curl, jq, bc
# ================================

# === Configuration ===

SHELLY_IP="192.168.1.60"
TELEGRAM_TOKEN="YOUR_REAL_TOKEN_HERE"
CHAT_ID="YOUR_REAL_CHAT_ID_HERE"

LOG_FILE="/home/youruser/system-scripts/cpu_fan.log"
LOG_OK_FILE="/home/youruser/system-scripts/cpu_fan_ok.log"
FAN_FLAG="/tmp/fan_control_by_script.flag"
TEMP_HOLD_FILE="/tmp/cpu_temp_hold.flag"
LOCK_FILE="/tmp/cpu_cooler_script.lock"

COOL_THRESHOLD=75
WARNING_THRESHOLD=80
REBOOT_THRESHOLD=85
REBOOT_HOLD_MINUTES=10

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# === Exit if manually locked ===
if [ -f "$LOCK_FILE" ]; then
  echo "$TIMESTAMP - Script is locked. Exiting." >> "$LOG_FILE"
  exit 0
fi

# === Dependencies check ===
for cmd in jq bc; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "$TIMESTAMP - ERROR: '$cmd' not found. Aborting." >> "$LOG_FILE"
    exit 1
  fi
done

# === Telegram Notification ===
send_telegram() {
  local MESSAGE="$1"
  curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$MESSAGE" >/dev/null
}

# === Get Shelly Fan Status ===
RESPONSE=$(curl -s --max-time 5 "http://${SHELLY_IP}/rpc/Switch.GetStatus?id=0")
if [ $? -ne 0 ] || [ -z "$RESPONSE" ]; then
  echo "$TIMESTAMP - ERROR: No response from Shelly." >> "$LOG_FILE"
  send_telegram "ERROR: Cannot reach Shelly relay."
  exit 1
fi

# === Validate Shelly JSON ===
if ! echo "$RESPONSE" | jq -e .output >/dev/null 2>&1; then
  echo "$TIMESTAMP - ERROR: Invalid Shelly response: $RESPONSE" >> "$LOG_FILE"
  send_telegram "ERROR: Unexpected Shelly response: $RESPONSE"
  exit 1
fi

FAN_STATUS=$(echo "$RESPONSE" | jq -r '.output')
CPU_TEMP=$(</sys/class/thermal/thermal_zone0/temp)
CPU_TEMP_C=$(awk "BEGIN {printf \"%.1f\", $CPU_TEMP/1000}")

log() {
  echo "$TIMESTAMP - $1" >> "$LOG_FILE"
}

# === CASE 1: Normal temperature ===
if (( $(echo "$CPU_TEMP_C < $COOL_THRESHOLD" | bc -l) )); then
  if [ "$FAN_STATUS" == "true" ] && [ -f "$FAN_FLAG" ]; then
    curl -s "http://${SHELLY_IP}/rpc/Switch.Set?id=0&on=false" >/dev/null
    rm -f "$FAN_FLAG"
    log "Temp ${CPU_TEMP_C}°C: Fan OFF by script."
    send_telegram "CPU cooled to ${CPU_TEMP_C}°C. Fan OFF."
  fi
  rm -f "$TEMP_HOLD_FILE"
  echo "$TIMESTAMP - All OK. CPU ${CPU_TEMP_C}°C." > "$LOG_OK_FILE"
  exit 0
fi

# === CASE 2: Warning zone ===
if (( $(echo "$CPU_TEMP_C >= $COOL_THRESHOLD && $CPU_TEMP_C < $WARNING_THRESHOLD" | bc -l) )); then
  log "Warning: CPU ${CPU_TEMP_C}°C"
  send_telegram "Warning: CPU at ${CPU_TEMP_C}°C."
  exit 0
fi

# === CASE 3: High temperature ===
if (( $(echo "$CPU_TEMP_C >= $WARNING_THRESHOLD && $CPU_TEMP_C < $REBOOT_THRESHOLD" | bc -l) )); then
  if [ "$FAN_STATUS" == "false" ]; then
    curl -s "http://${SHELLY_IP}/rpc/Switch.Set?id=0&on=true" >/dev/null
    touch "$FAN_FLAG"
    log "Temp ${CPU_TEMP_C}°C: Fan ON by script."
    send_telegram "CPU ${CPU_TEMP_C}°C. Fan turned ON."
  elif [ -f "$FAN_FLAG" ]; then
    log "Fan already ON by script. Temp ${CPU_TEMP_C}°C."
  fi
  rm -f "$TEMP_HOLD_FILE"
  exit 0
fi

# === CASE 4: Critical temperature ===
if (( $(echo "$CPU_TEMP_C >= $REBOOT_THRESHOLD" | bc -l) )); then
  if [ ! -f "$TEMP_HOLD_FILE" ]; then
    date +%s > "$TEMP_HOLD_FILE"
    log "Started hold for temp ${CPU_TEMP_C}°C"
    exit 0
  fi
  START=$(cat "$TEMP_HOLD_FILE")
  NOW=$(date +%s)
  DIFF=$((NOW - START))
  if (( DIFF >= REBOOT_HOLD_MINUTES * 60 )); then
    log "Reboot triggered: CPU ${CPU_TEMP_C}°C for $DIFF sec"
    send_telegram "CRITICAL: CPU ${CPU_TEMP_C}°C > $REBOOT_HOLD_MINUTES min. Rebooting."
    rm -f "$FAN_FLAG" "$TEMP_HOLD_FILE"
    reboot
  else
    log "Hold ongoing: CPU ${CPU_TEMP_C}°C for $DIFF sec"
  fi
  exit 0
fi

exit 0
