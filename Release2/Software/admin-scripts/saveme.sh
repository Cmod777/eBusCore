#!/bin/bash

# SaveMe.sh — Full System Backup to Remote Mac via SSH
# ----------------------------------------------------
# This script creates a complete backup of the Raspberry Pi's filesystem
# and transfers it to a remote Mac using SSH. It preserves permissions,
# shows progress (optional), and includes pre-checks and error handling.
#
# NOTE:
# This type of backup does NOT generate a bootable image, but
# it CAN be restored with standard procedures to replicate the system.
# For a fully bootable clone (bit-by-bit), a separate imaging script is required.
#
# Dependencies: sshpass, tar, pv (optional)
#
# Author: [Anonymous]
# License: MIT

### CONFIGURATION ###

# === REQUIRED ===
MAC_USER="your_mac_user"
MAC_PASS="your_mac_password"
MAC_IP="your_mac_ip"
MAC_FOLDER="/Users/$MAC_USER/Desktop/auto_RPI_backup"

# === BACKUP SETTINGS ===
BACKUP_NAME="rpi_backup_$(date +'%Y-%m-%d_%H-%M-%S').tar.gz"
BACKUP_FILE="/tmp/$BACKUP_NAME"
MIN_FREE_SPACE_MB=512
SHOW_PROGRESS=true  # Set to false to hide progress bar

# === OPTIONAL SSH KEY MODE ===
# Uncomment to use SSH keys instead of password (recommended)
# USE_SSH_KEY=true
# SSH_KEY_PATH="/home/pi/.ssh/id_rsa"

### OPTIONAL TELEGRAM NOTIFICATION ###
# TELEGRAM_BOT_TOKEN="xxxx"
# TELEGRAM_CHAT_ID="xxxx"

### START SCRIPT WITH SUDO IF NEEDED ###
if [ "$EUID" -ne 0 ]; then
  exec sudo "$0" "$@"
  exit
fi

### HELPER FUNCTIONS ###
log() { echo "[SaveMe] $1"; }
send_telegram() {
  [ -z "$TELEGRAM_BOT_TOKEN" ] && return
  curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d chat_id="$TELEGRAM_CHAT_ID" -d text="$1" >/dev/null
}

check_space() {
  local available_mb=$(df /tmp | awk 'NR==2 {print int($4/1024)}')
  if (( available_mb < MIN_FREE_SPACE_MB )); then
    log "ERROR: Not enough space on /tmp (${available_mb}MB available, required ${MIN_FREE_SPACE_MB}MB)"
    send_telegram "SaveMe ERROR: Insufficient space on /tmp"
    exit 1
  fi
}

ensure_package() {
  local pkg="$1"
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    log "Installing missing package: $pkg"
    apt update && apt install -y "$pkg"
  fi
}

### PRECHECKS ###
ensure_package sshpass
ensure_package pv

check_space

### STEP 1: CREATE BACKUP ARCHIVE ###
log "Creating full system backup archive..."
if [ "$SHOW_PROGRESS" = true ]; then
  tar --exclude="$BACKUP_FILE" \
      --exclude=/proc --exclude=/sys --exclude=/dev/pts --exclude=/run \
      -cvpzf - / | pv -n > "$BACKUP_FILE"
else
  tar --exclude="$BACKUP_FILE" \
      --exclude=/proc --exclude=/sys --exclude=/dev/pts --exclude=/run \
      -cvpzf "$BACKUP_FILE" /
fi

if [ $? -ne 0 ]; then
  log "ERROR: tar failed during archive creation"
  send_telegram "SaveMe ERROR: tar failed"
  exit 1
fi
log "Archive created: $BACKUP_FILE"

### STEP 2: CREATE DESTINATION ON MAC ###
log "Ensuring destination folder exists on remote Mac..."
sshpass -p "$MAC_PASS" ssh "$MAC_USER@$MAC_IP" "mkdir -p \"$MAC_FOLDER\""
if [ $? -ne 0 ]; then
  log "ERROR: Failed to create destination folder on Mac"
  send_telegram "SaveMe ERROR: mkdir failed on Mac"
  exit 1
fi

### STEP 3: TRANSFER BACKUP TO MAC ###
log "Transferring backup to Mac..."
sshpass -p "$MAC_PASS" rsync -avh --progress "$BACKUP_FILE" "$MAC_USER@$MAC_IP:\"$MAC_FOLDER/\""
if [ $? -ne 0 ]; then
  log "ERROR: Transfer failed"
  send_telegram "SaveMe ERROR: rsync failed"
  exit 1
fi

### STEP 4: CLEANUP ###
log "Cleaning up temporary archive..."
rm -f "$BACKUP_FILE"

log "Backup complete: $MAC_FOLDER/$BACKUP_NAME"
send_telegram "SaveMe SUCCESS: Backup transferred to $MAC_FOLDER/$BACKUP_NAME"

exit 0
