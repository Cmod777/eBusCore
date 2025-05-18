#!/bin/bash

# === BLOCK 0: LOAD ENVIRONMENT CONFIGURATION ===
ENV_FILE="$HOME/prometheus/.env.prometheus"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "$(date) - ENV file missing: $ENV_FILE" >> "/tmp/prometheus_env_error.log"
    exit 1
fi

echo "$(date) === SCRIPT STARTED ===" >> "$DEBUG_LOG"

# === GLOBAL VARIABLES ===
RUNNING=true
MODULATION_VALUES=()
MONITOR_PID=
CYCLE_COUNTER=0

# === TELEGRAM NOTIFICATION FUNCTION ===
send_telegram_notification() {
    local message="$1"
    echo "$(date) - Telegram: $message" >> "$DEBUG_LOG"
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="$message" > /dev/null 2>&1
    fi
}

# === UTILITY FUNCTIONS ===
try_command() {
    local cmd_array=("$@")
    local output=""
    local attempts=0

    while [ $attempts -lt 3 ]; do
        output=$("${cmd_array[@]}" 2>&1)
        if [ $? -eq 0 ] && [[ "$output" != *"ERR: SYN received"* ]]; then
            echo "$output"
            return 0
        fi
        ((attempts++))
        echo "$(date) - Attempt $attempts failed: ${cmd_array[*]}" >> "$ERROR_LOG_FILE"
        echo "$(date) - Output: $output" >> "$ERROR_LOG_FILE"
        sleep 2
    done

    echo "$(date) - Permanent failure: ${cmd_array[*]}" >> "$ERROR_LOG_FILE"
    echo "$(date) - Final output: $output" >> "$ERROR_LOG_FILE"
    return 1
}

is_number() {
    [[ "$1" =~ ^[0-9]+(\.[0-9]+)?$ ]]
}

# === GAS CALCULATION FUNCTION ===
calculate_gas_from_modulation() {
    local avg_mod="$1"
    local duration_sec="$2"

    if is_number "$avg_mod" && [[ "$duration_sec" =~ ^[0-9]+$ ]] && [ "$duration_sec" -gt 0 ]; then
        local power_watt=$(echo "scale=6; $MAX_POWER * $avg_mod / 100" | bc)
        local useful_watt=$(echo "scale=6; $power_watt * $BOILER_EFFICIENCY" | bc)
        local useful_mjh=$(echo "scale=6; $useful_watt * $WATT_TO_MJH" | bc)
        local hourly_gas=$(echo "scale=6; $useful_mjh / $GAS_LOWER_HEATING_VALUE" | bc)
        local raw_gas=$(echo "scale=6; $hourly_gas * $duration_sec / 3600" | bc)
        local adjusted_gas=$(echo "scale=6; $raw_gas * (1 + $CORRECTION_PERCENTAGE / 100)" | bc)
        printf "%.6f\n" "$adjusted_gas"
    else
        echo ""
        return 1
    fi
}

# === EVENT LOGGING ===
log_event() {
    local start="$1"
    local end="$2"
    local gas="$3"
    local avg_mod="$4"

    if ! [[ "$start" =~ ^[0-9]+$ && "$end" =~ ^[0-9]+$ ]]; then return 1; fi
    if ! is_number "$gas"; then return 1; fi

    local msg="{\"start\": 1, \"timestamp_start\": \"$(date -d @$start +'%Y-%m-%d %H:%M:%S')\", \
\"end\": 0, \"timestamp_end\": \"$(date -d @$end +'%Y-%m-%d %H:%M:%S')\", \
\"duration_sec\": $((end - start)), \
\"modulation_avg\": \"$avg_mod\", \
\"gas_consumed\": \"$gas m³\"}"

    echo "$msg" >> "$SUCCESS_LOG_FILE"
    send_telegram_notification "$msg"
}

# === MAIN MONITOR LOOP ===
monitor_heating_cycle() {
    echo "$(date) - monitor_heating_cycle started" >> "$DEBUG_LOG"
    local start_time=""
    local end_time=""
    local gas_used=""
    local flame_on=false
    local previous_flame="off"

    while [ "$RUNNING" = true ]; do
        if (( CYCLE_COUNTER % 2 == 0 )); then
            mod=$(try_command ssh YOUR_USER@YOUR_HOST docker exec YOUR_CONTAINER ebusctl read -f ModulationTempDesired)
            echo "$(date) - Modulation: $mod" >> "$DEBUG_LOG"
            if is_number "$mod" && [ "$flame_on" = true ]; then
                MODULATION_VALUES+=("$mod")
            fi
        else
            flame=$(try_command ssh YOUR_USER@YOUR_HOST docker exec YOUR_CONTAINER ebusctl read -f Flame)
            echo "$(date) - Flame: $flame" >> "$DEBUG_LOG"

            if [ "$flame" = "on" ] && [ "$previous_flame" = "off" ]; then
                start_time=$(date +%s)
                flame_on=true
                MODULATION_VALUES=()
                echo "$(date) - Flame ON (start_time: $start_time)" >> "$SUCCESS_LOG_FILE"

            elif [ "$flame" = "off" ] && [ "$flame_on" = true ]; then
                end_time=$(date +%s)
                flame_on=false

                local count=${#MODULATION_VALUES[@]}
                if [ "$count" -eq 0 ]; then
                    echo "$(date) - No modulation data collected." >> "$DEBUG_LOG"
                    start_time=""
                    previous_flame="$flame"
                    continue
                fi

                local sum=0
                for val in "${MODULATION_VALUES[@]}"; do
                    sum=$(echo "$sum + $val" | bc)
                done

                local avg=$(echo "scale=4; $sum / $count" | bc)
                local duration=$((end_time - start_time))
                gas_used=$(calculate_gas_from_modulation "$avg" "$duration")

                if [ $? -eq 0 ] && is_number "$gas_used"; then
                    log_event "$start_time" "$end_time" "$gas_used" "$avg"
                    echo "$(date) - Flame OFF, cycle ended (gas: $gas_used m³)" >> "$SUCCESS_LOG_FILE"
                else
                    echo "$(date) - Gas calc error. duration=$duration, avg=$avg" >> "$DEBUG_LOG"
                fi

                start_time=""
            fi

            previous_flame="$flame"
        fi

        ((CYCLE_COUNTER++))
        sleep 2
    done
}

# === SIGNAL HANDLING ===
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

# === EBUS STATUS CHECK ===
EBUS_STATE=$(ssh YOUR_USER@YOUR_HOST docker inspect --format='{{.State.Running}}' YOUR_CONTAINER 2>/dev/null | tr -d '\r')
if [ "$EBUS_STATE" != "true" ]; then
    echo "$(date) - eBUSd not active, starting..." >> "$DEBUG_LOG"
    try_command ssh YOUR_USER@YOUR_HOST docker start YOUR_CONTAINER
    sleep 5
else
    echo "$(date) - eBUSd already running" >> "$DEBUG_LOG"
fi

# === START MONITOR ===
echo "$(date) - Starting monitor process..." >> "$DEBUG_LOG"
monitor_heating_cycle &
MONITOR_PID=$!

wait "$MONITOR_PID"
(venv) ares@raspberrypi:~ $
