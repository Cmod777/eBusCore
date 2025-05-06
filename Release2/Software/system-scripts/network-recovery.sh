#!/bin/bash
# Script: network-recovery.sh
# Purpose: Automatically check for network connectivity and reboot if no connection is available.
# Usage: Add to crontab to run periodically, e.g., every 5 minutes.
# Example cron entry: */5 * * * * /home/<user>/system-scripts/network-recovery.sh

# Telegram notification settings (replace with your own values)
TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# Function to send Telegram message
send_telegram_message() {
  local message="$1"
  curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    -d chat_id="${CHAT_ID}" \
    -d text="${message}" > /dev/null
}

# Timestamp for logs and messages
NOW=$(date '+%Y-%m-%d %H:%M:%S')

# Check internet connectivity by pinging Google DNS
if ping -c 2 8.8.8.8 > /dev/null 2>&1; then
  echo "$NOW - Network OK" >> /home/<user>/system-scripts/network-recovery.log
else
  echo "$NOW - Network unreachable, rebooting..." >> /home/<user>/system-scripts/network-recovery.log
  send_telegram_message "Network issue detected - system will reboot ($NOW)"
  sudo /sbin/reboot
fi
