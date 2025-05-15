# ===============================================================
# SCRIPT NAME   : prometheus.sh
# VERSION       : 1.0
# AUTHOR        : Cmod777
# LICENSE       : See license.md for licensing information
#
# DESCRIPTION   :
#   Real-time gas usage estimation and monitoring for Vaillant eBUS boilers.
#   This script tracks modulation and flame activity, logs heating cycles,
#   and sends alerts via Telegram.
#
# REQUIREMENTS:
#   - SSH access to a system running ebusd in Docker
#   - curl (for Telegram integration)
#   - cron or other startup/watchdog mechanism
#
# CONFIGURABLE PARAMETERS (edit at top of script):
#
#   MAX_POWER_WATTS:
#       Nominal maximum power of your boiler in watts.
#       Check the technical datasheet of your boiler for the correct value.
#
#   MIN_GAS / MAX_GAS:
#       Minimum and maximum gas flow rates in cubic meters per hour (m³/h).
#       The minimum is usually set to 1.0 by default.
#       The maximum should be verified from the boiler's official specifications.
#
#   BOILER_EFFICIENCY:
#       Boiler efficiency factor (e.g., 0.99 for 99% efficiency).
#       This value should reflect real-world performance and may vary by model.
#
#   GAS_LOWER_HEATING_VALUE:
#       Lower heating value (PCI) of the gas used, in MJ/m³.
#       Default is 34.7 for methane. If using propane, LPG, or other fuels,
#       adjust accordingly based on official PCI values.
#
#   WATT_TO_MJH_CONVERSION:
#       Conversion factor from watts to megajoules per hour (MJ/h).
#       This is fixed for methane: 1 W = 0.0036 MJ/h.
#
#   TELEGRAM_BOT_TOKEN:
#       Your personal Telegram bot token for notifications (keep private).
#
#   TELEGRAM_CHAT_ID:
#       Your numeric Telegram chat ID to receive alerts.
#
# LOG FILES:
#   debug_prometheus.log      → Full runtime log (all events and errors)
#   prometheus_success.log    → Valid heating cycles with gas consumption
#   prometheus_errors.log     → Failed commands and SSH error traces
#
# SECURITY NOTICE:
#   This script has been scanned and verified using leakscan.py
#   to ensure that no sensitive tokens or keys are accidentally exposed.
#
# NOTES:
#   - Use crontab @reboot and a watchdog script to keep this running 24/7.
#   - Redact logs before publishing or sharing.
#   - Ensure SSH and Docker commands are working correctly before deployment.
# ===============================================================


# === BLOCK 1/3: SCRIPT INITIALIZATION AND SETUP ===
#!/bin/bash

# === ADVANCED DEBUG LOG ===
DEBUG_LOG="/-redacted-/youruser/ML_scripts/debug_prometheus.log"
echo "$(date) === SCRIPT START ===" >> "$DEBUG_LOG"

# === CONFIGURABLE PARAMETERS ===
MAX_POWER=24000
MIN_GAS=0.001
MAX_GAS=2.750
SUCCESS_LOG_FILE="/-redacted-/youruser/ML_scripts/prometheus_success.log"
ERROR_LOG_FILE="/-redacted-/youruser/ML_scripts/prometheus_errors.log"
DELAY_BETWEEN_ATTEMPTS=2
MAX_RETRIES=3
POLLING_INTERVAL=2
PING_TIMEOUT=2
BOILER_EFFICIENCY=0.99
GAS_LOWER_HEATING_VALUE=34.7
WATT_TO_MJH=0.0036

TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

RUNNING=true
MONITOR_PID=
MODULATION_PID=
MODULATION_VALUES=()

send_telegram_notification() {
    local message="$1"
    echo "$(date) - Telegram: $message" >> "$DEBUG_LOG"
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="$message" > /dev/null 2>&1
    fi
}

try_command() {
    local cmd_array=("$@")
    local attempts=0
    local output=""
    while [ $attempts -lt $MAX_RETRIES ]; do
        output=$("${cmd_array[@]}" 2>&1)
        if [ $? -eq 0 ] && [[ "$output" != *"ERR: SYN received"* ]]; then
            echo "$output"
            return 0
        fi
        ((attempts++))
        echo "$(date) - Attempt $attempts failed: ${cmd_array[*]}" >> "$ERROR_LOG_FILE"
        echo "$(date) - Command output: $output" >> "$ERROR_LOG_FILE"
        sleep "$DELAY_BETWEEN_ATTEMPTS"
    done
    echo "$(date) - Permanent failure: ${cmd_array[*]}" >> "$ERROR_LOG_FILE"
    echo "$(date) - Final output: $output" >> "$ERROR_LOG_FILE"
    return 1
}

is_number() {
    local num="$1"
    [[ "$num" =~ ^[0-9]+(\.[0-9]+)?$ ]]
}


# === BLOCK 2/3: CYCLES, CALCULATIONS, AND MODULATION ===

calculate_gas_from_modulation() {
    local avg_modulation="$1"
    local duration_sec="$2"

    if is_number "$avg_modulation" && [[ "$duration_sec" =~ ^[0-9]+$ ]] && [ "$duration_sec" -gt 0 ]; then
        local current_power_watt
        local useful_power_watt
        local useful_power_mjh
        local hourly_gas_usage
        local cycle_gas_usage

        current_power_watt=$(echo "scale=6; $MAX_POWER * $avg_modulation / 100" | bc)
        useful_power_watt=$(echo "scale=6; $current_power_watt * $BOILER_EFFICIENCY" | bc)
        useful_power_mjh=$(echo "scale=6; $useful_power_watt * $WATT_TO_MJH" | bc)
        hourly_gas_usage=$(echo "scale=6; $useful_power_mjh / $GAS_LOWER_HEATING_VALUE" | bc)
        cycle_gas_usage=$(echo "scale=6; $hourly_gas_usage * $duration_sec / 3600" | bc)

        printf "%.6f\n" "$cycle_gas_usage"
        return 0
    else
        echo ""
        return 1
    fi
}

log_event() {
    local start_time="$1"
    local end_time="$2"
    local gas_used="$3"

    if ! [[ "$start_time" =~ ^[0-9]+$ ]] || ! [[ "$end_time" =~ ^[0-9]+$ ]]; then
        return 1
    fi

    if [ -z "$gas_used" ] || ! is_number "$gas_used"; then
        return 1
    fi

    local log_message
    log_message="{\"start\": 1, \"timestamp_start\": \"$(date --date=@$start_time +'%Y-%m-%d %H:%M:%S')\", \"end\": 0, \"timestamp_end\": \"$(date --date=@$end_time +'%Y-%m-%d %H:%M:%S')\", \"duration_sec\": $((end_time - start_time)), \"gas_consumed_m3\": \"$gas_used\"}"

    echo "$log_message" >> "$SUCCESS_LOG_FILE"
    send_telegram_notification "$log_message"
    return 0
}


# === BLOCK 3/3: FLAME MONITORING, SIGNALS, AND STARTUP ===

monitor_heating_cycle() {
    echo "$(date) - monitor_heating_cycle started" >> "$DEBUG_LOG"
    local start_time=""
    local end_time=""
    local gas_used=""
    flame_on=false
    previous_flame_status="off"
    MODULATION_VALUES=()
    local cycle_counter=0

    while [ "$RUNNING" = true ]; do
        if (( cycle_counter % 2 == 0 )); then
            local mod_output
            mod_output=$(try_command ssh USER@HOST docker exec CONTAINER ebusctl read -f ModulationTempDesired)
            echo "$(date) - Modulation: $mod_output" >> "$DEBUG_LOG"
            if is_number "$mod_output" && [ "$flame_on" = true ]; then
                MODULATION_VALUES+=("$mod_output")
            fi
        else
            local flame_status_output
            flame_status_output=$(try_command ssh USER@HOST docker exec CONTAINER ebusctl read -f Flame)

            if [ $? -eq 0 ]; then
                local FLAME_STATUS="$flame_status_output"
                echo "$(date) - Flame status: $FLAME_STATUS" >> "$DEBUG_LOG"

                if [ "$FLAME_STATUS" = "on" ] && [ "$previous_flame_status" = "off" ]; then
                    start_time=$(date +%s)
                    flame_on=true
                    MODULATION_VALUES=()
                    echo "$(date) - Flame ON (start_time: $start_time)" >> "$SUCCESS_LOG_FILE"

                elif [ "$FLAME_STATUS" = "off" ] && [ "$flame_on" = true ]; then
                    end_time=$(date +%s)
                    flame_on=false

                    local count=${#MODULATION_VALUES[@]}
                    if [ "$count" -eq 0 ]; then
                        echo "$(date) - No valid modulation data collected." >> "$DEBUG_LOG"
                        start_time=""
                        previous_flame_status="$FLAME_STATUS"
                        continue
                    fi

                    local sum=0
                    for val in "${MODULATION_VALUES[@]}"; do
                        sum=$(echo "$sum + $val" | bc)
                    done
                    local avg=$(echo "scale=4; $sum / $count" | bc)
                    local duration_sec=$((end_time - start_time))

                    if [ "$duration_sec" -le 0 ]; then
                        echo "$(date) - Invalid cycle duration: $duration_sec sec" >> "$DEBUG_LOG"
                        start_time=""
                        previous_flame_status="$FLAME_STATUS"
                        continue
                    fi

                    gas_used=$(calculate_gas_from_modulation "$avg" "$duration_sec")
                    if [ $? -eq 0 ] && is_number "$gas_used" && [ -n "$gas_used" ]; then
                        log_event "$start_time" "$end_time" "$gas_used"
                        echo "$(date) - Flame OFF, cycle complete (gas: $gas_used m³)" >> "$SUCCESS_LOG_FILE"
                    else
                        echo "$(date) - Gas calculation error: duration=$duration_sec avg=$avg" >> "$DEBUG_LOG"
                    fi

                    start_time=""
                fi

                previous_flame_status="$FLAME_STATUS"
            fi
        fi

        ((cycle_counter++))
        sleep 2
    done
}

handle_sigterm() {
    echo "$(date) - SIGTERM received" >> "$DEBUG_LOG"
    RUNNING=false
    [ -n "$MONITOR_PID" ] && kill "$MONITOR_PID"
}

handle_sigquit() {
    echo "$(date) - SIGQUIT received" >> "$DEBUG_LOG"
    RUNNING=false
    [ -n "$MONITOR_PID" ] && kill -9 "$MONITOR_PID"
    exit 1
}

trap handle_sigterm SIGINT SIGTERM
trap handle_sigquit SIGQUIT

echo "$(date) - Initial checks" >> "$DEBUG_LOG"

EBUS_STATUS=$(ssh USER@HOST docker inspect --format='{{.State.Running}}' 'CONTAINER' 2>/dev/null | tr -d '\r')

if [ "$EBUS_STATUS" = "true" ]; then
    echo "$(date) - eBUSd already running" >> "$DEBUG_LOG"
elif [ "$EBUS_STATUS" = "false" ]; then
    echo "$(date) - Starting eBUSd..." >> "$DEBUG_LOG"
    try_command ssh USER@HOST docker start 'CONTAINER'
    sleep 5
else
    echo "$(date) - Invalid eBUSd state or command failed (EBUS_STATUS='$EBUS_STATUS')" >> "$DEBUG_LOG"
    exit 1
fi

echo "$(date) - Launching monitor in background" >> "$DEBUG_LOG"
monitor_heating_cycle &
MONITOR_PID=$!

if [ -n "$MONITOR_PID" ] && [[ "$MONITOR_PID" =~ ^[0-9]+$ ]]; then
    wait "$MONITOR_PID"
fi
