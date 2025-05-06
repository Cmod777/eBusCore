#!/bin/bash

# ------------------------------------------
# Daily Reboot Script with Telegram Notification
# Author: [YourName or Anonymous]
# Add to crontab with:
#   0 3 * * * /path/to/script/daily-reboot.sh
# (performs a reboot every day at 03:00 AM)
# ------------------------------------------

# Insert your Telegram bot token here
TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

# Insert your Telegram chat ID here
CHAT_ID="YOUR_CHAT_ID"

# Get current time
TIME=$(date '+%H:%M on %d/%m/%Y')

# Message to send
MESSAGE="Raspberry Pi: scheduled reboot completed at $TIME"

# Send Telegram notification
curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -d chat_id="$CHAT_ID" \
  -d text="$MESSAGE" \
  -d parse_mode="Markdown"

# Reboot the system
/sbin/reboot
