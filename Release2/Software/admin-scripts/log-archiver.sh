#!/bin/bash
# Script: log-archiver.sh
# Purpose: Monthly archive and compress all .log files from the system-scripts directory.
#          Sends a Telegram message and updates a dedicated archive log.
# Usage: Recommended schedule: once per month.
# Example cron entry: 0 3 1 * * /home/<user>/admin-scripts/log-archiver.sh

# Telegram configuration (replace with your credentials)
TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# Directories
SCRIPT_DIR="/home/<user>/system-scripts"
ARCHIVE_DIR="/home/<user>/admin-scripts/ARCHIVE_LOG"
LOG_FILE="/home/<user>/admin-scripts/log-archiver.log"

# Timestamp
NOW=$(date '+%Y-%m-%d %H:%M:%S')
ARCHIVE_TAG=$(date '+%Y%m%d_%H%M%S')

# Create archive directory if not exists
mkdir -p "$ARCHIVE_DIR"

# Archive log
echo "$NOW - Starting log archive process" >> "$LOG_FILE"

# Find and process each .log file
for logfile in "$SCRIPT_DIR"/*.log; do
  if [ -f "$logfile" ]; then
    base=$(basename "$logfile")
    archive_name="${base%.log}_$ARCHIVE_TAG.log"
    cp "$logfile" "$ARCHIVE_DIR/$archive_name"
    gzip "$ARCHIVE_DIR/$archive_name"
    echo "$NOW - Archived $base as $archive_name.gz" >> "$LOG_FILE"
    echo "$NOW - [ARCHIVED] This log was moved to $ARCHIVE_DIR/$archive_name.gz" > "$logfile"
  fi
done

# Send Telegram notification
MSG="Log archive completed at $NOW.
Archived logs from $SCRIPT_DIR to $ARCHIVE_DIR."
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="$MSG" > /dev/null
