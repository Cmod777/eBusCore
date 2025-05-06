#!/usr/bin/env bash
# SaveMeImage.sh - Full Raspberry Pi Backup Script
#
# Description:
#   Connects to a remote Raspberry Pi via SSH, reads a raw bitwise image
#   of the SD card, streams it over the network, displays a local
#   progress bar, compresses the data, and saves it locally.
#   After transfer, it cleans up any temporary files on the Pi.
#
#  This script is created to be used preferably with these prerequisites:
#    - macOS with Homebrew installed (or another package manager)
#    - SSH access to the Raspberry Pi (password or key-based)
#  It can be modified to suit other environments.
# Usage:
#   1. Copy this script to your local machine.
#   2. Make it executable: chmod +x SaveMeImage.sh
#   3. Edit configuration variables below or set them
#      as environment variables.
#   4. Run: ./SaveMeImage.sh
#
# Configuration Variables:
#   RPI_USER     - SSH username for Raspberry Pi
#   RPI_PASS     - SSH password (if using password auth)
#   RPI_HOST     - Hostname or IP of Raspberry Pi
#   SSH_KEY_PATH - Path to private SSH key (for key auth)
#   IMG_PREFIX   - Prefix for backup image filename
#   LOCAL_SAVE_DIR - Directory to store backups and logs locally

set -euo pipefail
IFS=$'\n\t'

# Load configuration from environment or use defaults
RPI_USER="${RPI_USER:-pi}"
RPI_PASS="${RPI_PASS:-your_password_here}"
RPI_HOST="${RPI_HOST:-raspberrypi.local}"
SSH_KEY_PATH="${SSH_KEY_PATH:-$HOME/.ssh/id_rsa}"
IMG_PREFIX="${IMG_PREFIX:-rpi_full_backup}"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
IMG_NAME="${IMG_PREFIX}_${TIMESTAMP}.img.gz"
LOCAL_SAVE_DIR="${LOCAL_SAVE_DIR:-$HOME/Desktop/auto_RPI_backup}"
LOCAL_IMG_PATH="$LOCAL_SAVE_DIR/$IMG_NAME"
LOG_FILE="$LOCAL_SAVE_DIR/backup_log.txt"

echo "$(date +'%Y-%m-%d %H:%M:%S') - Starting Raspberry Pi backup" | tee -a "$LOG_FILE"

# Ensure local save directory exists
mkdir -p "$LOCAL_SAVE_DIR"

# Build SSH command with key or password fallback
ssh_base=(ssh -o BatchMode=yes -o StrictHostKeyChecking=no)
rsync_base="rsync --progress -e ssh"
if [[ -f "$SSH_KEY_PATH" ]]; then
  ssh_base+=( -i "$SSH_KEY_PATH" )
  rsync_base="rsync --progress -e \"ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no\""
  echo "Using SSH key authentication" | tee -a "$LOG_FILE"
elif command -v sshpass &>/dev/null; then
  ssh_base=(sshpass -p "$RPI_PASS" ssh -o StrictHostKeyChecking=no)
  rsync_base="rsync --progress -e \"sshpass -p $RPI_PASS ssh -o StrictHostKeyChecking=no\""
  echo "Using password authentication" | tee -a "$LOG_FILE"
else
  echo "ERROR: No SSH key found and sshpass not installed" | tee -a "$LOG_FILE"
  exit 1
fi

# Test SSH connectivity
if ! "${ssh_base[@]}" "$RPI_USER@$RPI_HOST" echo Connected &>/dev/null; then
  echo "ERROR: Cannot connect to $RPI_HOST via SSH" | tee -a "$LOG_FILE"
  exit 1
fi

echo "SSH connection to $RPI_HOST succeeded" | tee -a "$LOG_FILE"

# Detect remote disk device
disk=$("${ssh_base[@]}" "$RPI_USER@$RPI_HOST" \
  "lsblk -ndo NAME,TYPE | awk '\$2==\"disk\"{print \"/dev/\"\$1; exit}'")
if [[ -z "$disk" ]]; then
  echo "ERROR: Unable to detect disk on remote Pi" | tee -a "$LOG_FILE"
  exit 1
fi

echo "Remote disk detected: $disk" | tee -a "$LOG_FILE"

# Get remote disk size for progress bar
size=$("${ssh_base[@]}" "$RPI_USER@$RPI_HOST" "sudo blockdev --getsize64 $disk")
if [[ -z "$size" ]]; then
  echo "ERROR: Unable to retrieve disk size" | tee -a "$LOG_FILE"
  exit 1
fi

echo "Remote disk size: $size bytes" | tee -a "$LOG_FILE"

# Stream raw disk data over SSH, show local progress, compress locally
echo "Beginning image creation and transfer..." | tee -a "$LOG_FILE"
"${ssh_base[@]}" "$RPI_USER@$RPI_HOST" "sudo dd if=$disk bs=4M status=none" \
  | pv -s "$size" \
  | gzip -1 > "$LOCAL_IMG_PATH"

echo "Image stream and compression complete" | tee -a "$LOG_FILE"

echo "Backup image saved to: $LOCAL_IMG_PATH" | tee -a "$LOG_FILE"

echo "Raspberry Pi backup finished successfully." | tee -a "$LOG_FILE"
exit 0
