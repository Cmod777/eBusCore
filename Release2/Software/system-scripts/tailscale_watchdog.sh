#!/bin/bash

# Service to monitor
SERVICE="tailscaled"

# Telegram bot token and chat ID
TOKEN="ADD_YOUR_TOKEN"
CHAT_ID="ADD_YOUR_ID"

# Check if the service is running
if ! systemctl is-active --quiet $SERVICE; then
    # Restart the service
    systemctl restart $SERVICE

    # Send Telegram notification
    MESSAGE="Tailscale was automatically restarted on the Raspberry Pi."
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MESSAGE"
fi
