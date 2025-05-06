#!/bin/bash
# Script: storage-health-check.sh
# Purpose: Monitor disk space and alert if any filesystem exceeds a defined usage threshold.
# Usage: Schedule via cron, e.g., every 10 minutes.
# Example cron entry: */10 * * * * /home/<user>/system-scripts/storage-health-check.sh

# Telegram configuration (replace with your actual credentials)
TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# Threshold percentage (e.g., alert if disk usage >= 85%)
THRESHOLD=85

# Function to send a Telegram alert
send_telegram_message() {
  local message="$1"
  curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    -d chat_id="${CHAT_ID}" \
    -d text="${message}" > /dev/null
}

# Timestamp for logs
NOW=$(date '+%Y-%m-%d %H:%M:%S')
LOGFILE="/home/<user>/system-scripts/storage-health.log"

# Check disk usage and trigger alert if any mount exceeds threshold
ALERTS=()
while read -r line; do
  usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
  mountpoint=$(echo "$line" | awk '{print $6}')
  if [ "$usage" -ge "$THRESHOLD" ]; then
    ALERTS+=("$mountpoint is at ${usage}%")
  fi
done <<< "$(df -h --output=pcent,target | tail -n +2)"

if [ ${#ALERTS[@]} -eq 0 ]; then
  echo "$NOW - Disk usage within safe limits" >> "$LOGFILE"
else
  for alert in "${ALERTS[@]}"; do
    msg="$NOW - WARNING: $alert"
    echo "$msg" >> "$LOGFILE"
    send_telegram_message "$msg"
  done
fi
