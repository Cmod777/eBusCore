#!/bin/bash

# Shelly IP and Telegram configuration
SHELLY_IP="YOUR_SHELLY_IP"  # Replace with your Shelly device's IP address
TOKEN="YOUR_BOT_TOKEN"  # Replace with your Telegram bot token
CHAT_ID="YOUR_CHAT_ID"  # Replace with your Telegram chat ID

# File to store the last known state
STATE_FILE="/tmp/shelly_fan_state.txt"

# Get the current state of the relay (true = ON / false = OFF)
CURRENT_STATE=$(curl -s http://$SHELLY_IP/rpc/Switch.GetStatus?id=0 | jq -r '.output')

# If the state is null (error), exit the script
if [ -z "$CURRENT_STATE" ]; then
  echo "Error: Unable to retrieve state from Shelly"
  exit 1
fi

# Retrieve the previous state if it exists
if [ -f "$STATE_FILE" ]; then
    LAST_STATE=$(cat "$STATE_FILE")
else
    LAST_STATE=""
fi

# If the state has changed, send a Telegram notification
if [ "$CURRENT_STATE" != "$LAST_STATE" ]; then
    if [ "$CURRENT_STATE" == "true" ]; then
        MESSAGE="FAN ACTIVATED: Forced ventilation started!"
    else
        MESSAGE="FAN DEACTIVATED: Temperature returned to normal."
    fi

    # Send the notification to Telegram
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MESSAGE"

    # Save the current state to the state file
    echo "$CURRENT_STATE" > "$STATE_FILE"
fi
