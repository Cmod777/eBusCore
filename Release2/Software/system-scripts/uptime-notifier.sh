#!/bin/bash
# Script: uptime-notifier.sh
# Purpose: Send periodic notification with hostname and uptime via Telegram.
# Usage: Schedule via cron, e.g., every 2 days at 09:00.
# Example cron entry: 0 9 */2 * * /home/<user>/system-scripts/uptime-notifier.sh

# Telegram configuration (replace with your real credentials)
TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# Prepare data
HOSTNAME=$(hostname)
UPTIME=$(uptime -p)
NOW=$(date '+%Y-%m-%d %H:%M:%S')

# Format message
MESSAGE="Uptime report ($NOW):
Host: $HOSTNAME
Uptime: $UPTIME"

# Send message via Telegram
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="$MESSAGE" > /dev/null
