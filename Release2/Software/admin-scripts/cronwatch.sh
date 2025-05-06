#!/bin/bash

# === CRONWATCH - System Cron Monitor Script ===
# Monitors all cron jobs (from user/root crontabs and system cron directories)
# and checks whether they have executed as expected using syslog timestamps.
# If a job is missing or hasn't run within a threshold, it triggers a log entry and a Telegram notification.

# --- Notes for GitHub ---
# This script assumes:
# 1. The system uses traditional syslog (/var/log/syslog).
#    On Debian/Raspberry Pi OS, you may need to install it:
#       sudo apt install rsyslog
#
# 2. You should let the system run for **24–48 hours** before trusting the first output,
#    to allow daily/weekly/monthly cron jobs to run at least once.
#
# 3. Cron jobs managed by `anacron` may not appear in syslog or be tracked precisely.
#
# 4. This tool provides a good approximation but **can generate false positives**
#    for rarely executed jobs or conditional command wrappers (e.g. `test -x ... || { ... }`).

# === Configuration ===
TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

LOG_OK="/home/youruser/admin-scripts/cronwatch_ok.log"
LOG_ERR="/home/youruser/admin-scripts/cronwatch_error.log"
TMP_CRONS="/tmp/cronjobs.txt"
TMP_SYSLOG="/tmp/cron_syslog.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

WARN_THRESHOLD_MIN=120    # Warn if job hasn't run in 2+ hours
CRIT_THRESHOLD_MIN=360    # Critical if not run in 6+ hours

# === Functions ===

send_telegram() {
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$1" >/dev/null
}

log_ok() {
    echo "$TIMESTAMP - All cron jobs verified." > "$LOG_OK"
}

log_error() {
    echo "$TIMESTAMP - $1" >> "$LOG_ERR"
}

print_progress() {
    echo "[${1}/4] $2"
    sleep 0.5
}

# === Main Logic ===

echo "=== CRONWATCH STARTED ==="

print_progress 1 "Collecting cron jobs..."
{
    crontab -l 2>/dev/null
    sudo crontab -l -u root 2>/dev/null
    grep -v '^#' /etc/crontab 2>/dev/null
    find /etc/cron.d/ -type f -exec grep -v '^#' {} \; 2>/dev/null
} | awk '{ if (NF > 5) print substr($0, index($0,$6)) }' | sort | uniq > "$TMP_CRONS"

print_progress 2 "Analyzing recent cron executions..."
if [ -f /var/log/syslog ]; then
    grep CRON /var/log/syslog | grep -v "session opened" > "$TMP_SYSLOG"
else
    echo "Syslog not found. Skipping cron log analysis."
    > "$TMP_SYSLOG"
fi

print_progress 3 "Matching jobs with syslog timestamps..."
WARNINGS=0
CRITICALS=0

while read -r COMMAND; do
    LAST_RUN=$(grep -F "$COMMAND" "$TMP_SYSLOG" | tail -n1 | cut -d ' ' -f1-3)
    if [ -z "$LAST_RUN" ]; then
        log_error "NEVER executed: $COMMAND"
        ((CRITICALS++))
        continue
    fi
    LAST_TS=$(date -d "$LAST_RUN" +%s 2>/dev/null)
    NOW_TS=$(date +%s)
    DIFF=$(( (NOW_TS - LAST_TS) / 60 ))

    if (( DIFF > CRIT_THRESHOLD_MIN )); then
        log_error "Missed: $COMMAND (last run $DIFF minutes ago)"
        ((CRITICALS++))
    elif (( DIFF > WARN_THRESHOLD_MIN )); then
        log_error "Delayed: $COMMAND (last run $DIFF minutes ago)"
        ((WARNINGS++))
    fi
done < "$TMP_CRONS"

print_progress 4 "Finalizing..."

if (( CRITICALS > 0 )); then
    send_telegram "CRONWATCH CRITICAL: $CRITICALS job(s) missed or never run. See log."
    exit 1
elif (( WARNINGS > 0 )); then
    send_telegram "CRONWATCH WARNING: $WARNINGS job(s) possibly delayed. See log."
    exit 0
else
    log_ok
    send_telegram "CRONWATCH: All cron jobs executed as expected."
fi

# Cleanup
rm -f "$TMP_CRONS" "$TMP_SYSLOG"
exit 0

# NOTE: This script currently monitors only traditional cron jobs (from crontab, /etc/cron.d/, etc.).
# Optionally, you may extend it to include:
# - @reboot jobs: These are executed once at system startup and are not tied to a regular schedule.
# - systemd timers: Many modern systems (e.g. Debian Bookworm, Ubuntu) use systemd timers as a replacement for cron.
#   These timers are managed via `.timer` and `.service` files and can be listed with `systemctl list-timers`.
# Adding support for these would allow broader and more complete monitoring of scheduled tasks across the system.
