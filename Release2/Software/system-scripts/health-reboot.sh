#!/bin/bash

# ----------------------------------------------
# Health check reboot script with optional Telegram alert
# Logs every execution; triggers reboot only on failure
# Designed for headless Raspberry Pi or similar systems
# Recommended to run via crontab every 1–5 minutes
# ----------------------------------------------

# === Telegram Configuration ===
# Replace with your bot token and chat ID if you want alerts
TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# === Log File ===
LOGFILE="/path/to/your/log/health-reboot.log"

# === Enable or disable individual checks ===
CHECK_NETWORK=true
CHECK_TMP_WRITE=true
CHECK_FS_READONLY=true
CHECK_RAM=true
CHECK_ZOMBIES=true

# === Utility Functions ===
log() {
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  echo "$TIMESTAMP - $1" >> "$LOGFILE"
}

send_telegram() {
  local MESSAGE="$1"
  local TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="[$TIMESTAMP] $MESSAGE" \
    -d parse_mode="Markdown"
}

# === Health Checks ===

# 1. Network connectivity
if $CHECK_NETWORK; then
  ping -c1 8.8.8.8 >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    log "Trigger: Network unreachable"
    send_telegram "Health reboot triggered: *Network unreachable*. Rebooting..."
    /sbin/reboot
  fi
fi

# 2. Writable /tmp
if $CHECK_TMP_WRITE; then
  touch /tmp/health-testfile && rm /tmp/health-testfile || {
    log "Trigger: /tmp not writable"
    send_telegram "Health reboot triggered: */tmp not writable*. Rebooting..."
    /sbin/reboot
  }
fi

# 3. Root filesystem read-only
if $CHECK_FS_READONLY; then
  mount | grep ' on / ' | grep -q 'ro,' && {
    log "Trigger: Root filesystem is read-only"
    send_telegram "Health reboot triggered: *Root filesystem is read-only*. Rebooting..."
    /sbin/reboot
  }
fi

# 4. Low available RAM
if $CHECK_RAM; then
  FREE_RAM=$(free -m | awk '/^Mem:/ { print $7 }')
  if [ "$FREE_RAM" -lt 20 ]; then
    log "Trigger: Low available RAM: ${FREE_RAM}MB"
    send_telegram "Health reboot triggered: *Low available RAM (${FREE_RAM}MB)*. Rebooting..."
    /sbin/reboot
  fi
fi

# 5. Excessive zombie processes
if $CHECK_ZOMBIES; then
  ZOMBIE_COUNT=$(ps aux | awk '{ if ($8 == "Z") print }' | wc -l)
  if [ "$ZOMBIE_COUNT" -gt 5 ]; then
    log "Trigger: Zombie processes detected: $ZOMBIE_COUNT"
    send_telegram "Health reboot triggered: *Excessive zombie processes ($ZOMBIE_COUNT)*. Rebooting..."
    /sbin/reboot
  fi
fi

# === If all checks passed ===
log "Health check completed: no issues detected"
