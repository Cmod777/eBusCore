#!/bin/bash
# Script: self-heal-update.sh
# Purpose: Automatically apply system updates and notify via Telegram.
# Usage: Add to crontab to run daily or weekly, depending on preference.
# Example cron entry: 0 4 * * * /home/<user>/system-scripts/self-heal-update.sh

# Telegram credentials (replace with your real values)
TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# Logging and timestamp
NOW=$(date '+%Y-%m-%d %H:%M:%S')
LOGFILE="/home/<user>/system-scripts/self-heal-update.log"

# Function to send Telegram message
send_telegram_message() {
  local message="$1"
  curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    -d chat_id="${CHAT_ID}" \
    -d text="${message}" > /dev/null
}

echo "$NOW - Starting system update" >> "$LOGFILE"

# Run the system update commands
sudo apt update >> "$LOGFILE" 2>&1
sudo apt upgrade -y >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
  MSG="$NOW - System updated successfully"
else
  MSG="$NOW - System update encountered an error"
fi

echo "$MSG" >> "$LOGFILE"
send_telegram_message "$MSG"
