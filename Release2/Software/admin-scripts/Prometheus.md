# Prometheus Monitoring System – Project Overview

This project was inspired by the excellent work of [john30/ebusd](https://github.com/john30/ebusd) and [john30/ebusd-esp32](https://github.com/john30/ebusd-esp32), particularly the integration of an ESP32-based eBUS WiFi module connected directly to the boiler. We took this as a foundation and extended it by building a dedicated control unit (described in other sections of this repository) to enhance data monitoring and reliability.

While Home Assistant supports MQTT autodiscovery and `ebusd` integration, we observed critical limitations:
- The autodiscovery did not expose all boiler parameters.
- Some registers (e.g., `Flame`, `Gasvalve`) were either not shown or only returned stale cached values.
- Commands that should return real-time data appeared inactive or unresponsive through the standard interface.

We solved this by identifying the correct configuration file for our boiler (`bai.308523.inc`) and accessing the values directly using forced command-line calls to `ebusctl`, bypassing autodiscovery where necessary.

This hybrid approach allows us to:
- Use Home Assistant as the automation platform.
- Extract precise boiler data (especially for gas/flame cycles) via shell commands.
- Log events externally, enabling accurate tracking of gas consumption, flame activity, and system behavior.

---

## Verified eBUSD Commands for Flame Status

```bash
# 1. Real-time Flame state (bypasses cache)
docker exec -it <ebusd_container_name> ebusctl read -f Flame

# Returns:
# → "on"  = boiler is burning gas
# → "off" = boiler is idle

# 2. Repeat while hot water or heating is active
docker exec -it <ebusd_container_name> ebusctl read -f Flame

# 3. (Optional) Check Gasvalve status
docker exec -it <ebusd_container_name> ebusctl read -f Gasvalve

# 4. List registers containing 'flame' or 'gas'
docker exec -it <ebusd_container_name> ebusctl find | grep -i flame
docker exec -it <ebusd_container_name> ebusctl find | grep -i gas
```

---

## Diagnostic Recap – Flame Register Troubleshooting

```bash
# First attempt: failed (no -f flag)
docker exec -it <ebusd_container_name> ebusctl read Flame

# Result: always "off", even during combustion

# Second attempt: list active commands
docker exec -it <ebusd_container_name> ebusctl find -f on

# Result: Flame and Gasvalve not listed

# Third attempt: check BAI circuit
docker exec -it <ebusd_container_name> ebusctl find | grep bai

# Result: mostly "no data stored" → suspected circuit lock

# Final working command:
docker exec -it <ebusd_container_name> ebusctl read -f Flame

# ✅ Result: returns "on" during combustion, "off" at rest
# → Confirmed working and reliable
```

**Conclusion:** The only reliable way to read the `Flame` state is with:

```bash
docker exec -it <ebusd_container_name> ebusctl read -f Flame
```

Avoid using the command **without `-f`**, as it may return outdated or cached values.

---

## Bidirectional SSH Link – Raspberry Pi ↔ Home Assistant

### 1. SSH Key Created on Home Assistant
- User: `homeassistant_user`  
- IP: `HOME_ASSISTANT_IP`  
- Key path: `/-redacted-/-redacted-/id_rsa.pub`

> NOTE: standard path shown for educational purposes – never expose real keys in public repositories.

### 2. Key Copied to Raspberry Pi (`raspberry_user@RASPBERRY_IP`)
```bash
cat ~/-redacted-/id_rsa.pub | ssh raspberry_user@RASPBERRY_IP \
  "mkdir -p ~/-redacted- && cat >> ~/-redacted-/authorized_keys && chmod 700 ~/-redacted- && chmod 600 ~/-redacted-/authorized_keys"
```

Now Home Assistant can access the Raspberry Pi without a password:
```bash
ssh raspberry_user@RASPBERRY_IP
```

### 3. Raspberry Access to Home Assistant (`homeassistant_user@HOME_ASSISTANT_IP`)
```bash
cat ~/-redacted-/id_rsa.pub | ssh homeassistant_user@HOME_ASSISTANT_IP \
  "mkdir -p ~/-redacted- && cat >> ~/-redacted-/authorized_keys && chmod 700 ~/-redacted- && chmod 600 ~/-redacted-/authorized_keys"
```

Now Raspberry Pi can access Home Assistant with:
```bash
ssh homeassistant_user@HOME_ASSISTANT_IP
```

### 4. Bidirectional Access Verified
Both directions confirmed working without passwords.

### 5. Remote Commands from Raspberry Pi
Example – Read boiler flame state:
```bash
ssh homeassistant_user@HOME_ASSISTANT_IP \
  "docker exec -i <ebusd_container_name> ebusctl read -f Flame"
```

**Confirmed:** Real-time `on` / `off` response.

---

## Future Use

This SSH link allows the Raspberry Pi to:
- Query Home Assistant remotely
- Extract real-time data from `ebusd`
- Log everything locally without relying on MQTT or Home Assistant sensors

---

## Block 1 – System Description

The **Prometheus** system is an advanced Bash script for the automatic monitoring of estimated natural gas consumption on **Vaillant eBUS** boilers, with analysis of **modulation** and **flame** status. It is designed to:

- Start automatically upon system boot.
- Execute a continuous and self-healing cycle.
- Estimate gas consumption in **m³** for each flame ignition.
- Write each event to a `.log` file and send a real-time **Telegram alert**.
- Operate 24/7 even in case of reboots, crashes, or temporary issues.

### Main Features

- **Automatic startup** via `@reboot` in `crontab`.
- **Watchdog** every 60s: detects zombie or missing processes.
- **Weekly cleanup** of the debug log.
- **Simplified self-diagnosis** through log analysis.
- **Alternating data cycle**: reads `Modulation` and `Flame` every 2s sequentially.

### Requirements

- **Operating system**: Debian-based (e.g., Raspberry Pi OS)
- **Active eBUS interface**
- **Active SSH connection** to the system with `ebusd` Docker
- **Access to crontab and script execution permissions**
- Valid Telegram bot token and chat ID

> ⚠️ Note: Be careful not to publish actual Telegram tokens or chat IDs in public repositories.

### Involved Components

| Component                  | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `prometheus.sh`            | Main script, performs continuous monitoring and calculation logic         |
| `run_prometheus.sh`        | Watchdog: verifies that `prometheus.sh` is active, restarts it if necessary |
| `debug_prometheus.log`     | Debug log with all events and readings                                 |
| `prometheus_success.log`   | Log of cycles with valid calculations and sent notifications                        |
| `crontab`                  | Manages automatic startup, watchdog, and weekly cleanup                   |
| `clean_prometheus_debug.sh`| Weekly empties the debug log to prevent disk filling        |



# Block 2 – Data Flow and Internal Operation

## 1. Operational Cycle

The core of the `prometheus.sh` script is an infinite `while` loop alternating every 2 seconds between two main operations:

- **Reading modulation** (`ModulationTempDesired`)
- **Reading flame status** (`Flame`)

This structure allows efficient staggered data collection, avoiding overlaps or simultaneous reads.

### Sequential Cycle

| Seconds | Operation          |
|---------|--------------------|
| 0       | Read `Modulation`  |
| 2       | Read `Flame`       |
| 4       | Read `Modulation`  |
| 6       | Read `Flame`       |
| ...     | ...                |

## 2. State Handling

### Ignition

When the flame changes from `off` to `on`, the script:

- Records the **start timestamp**
- Clears the `MODULATION_VALUES` array
- Sets `flame_on=true`

### During Ignition

- On each even-numbered cycle, if `flame_on=true`, the current modulation is added to the array.
- The array will be used to calculate the **average modulation** later.

### Shutdown

When the flame switches back to `off`, the script:

- Records the **end timestamp**
- Calculates the **total duration**
- Calculates the **average modulation**
- Estimates **gas consumption (m³)** using the `calculate_gas_from_modulation` function
- Logs everything into `prometheus_success.log` and sends a Telegram message

## 3. Gas Calculation Formula

```bash
gas_m3 = ((MAX_POWER * modulation_percent / 100) * efficiency * 0.0036 / PCI) * (duration_sec / 3600)
```

**Parameters:**

- `MAX_POWER` = 24000 W  
- `EFFICIENCY` = 0.99  
- `WATT_TO_MJH` = 0.0036  
- `PCI (Lower Heating Value of Gas)` = 34.7 MJ/m³

> ⚠️ The values shown for `MAX_POWER`, `EFFICIENCY`, and `PCI` are examples. Always refer to your boiler's official technical documentation to verify the correct parameters for your specific model.

## 4. Telegram Notifications

Each completed event includes:

- Start and end timestamp  
- Total time in seconds  
- Estimated gas usage in cubic meters

> ⚠️ Ensure your Telegram bot token and chat ID are kept private and never committed to public repositories.
---

# Block 3 – Watchdog and Automatic Protection

## 1. Automatic Startup on Boot

The script is automatically launched at system boot using `@reboot` in the `crontab`:

```cron
@reboot nohup bash /-redacted-/youruser/ML_scripts/prometheus.sh >> /-redacted-/youruser/ML_scripts/debug_prometheus.log 2>&1 &
```

This ensures that every time the Raspberry Pi is powered on or rebooted, the script starts automatically.

## 2. Minute-Based Watchdog

The script `run_prometheus.sh` checks every minute whether `prometheus.sh` is running. If it’s not found among active processes, it will be restarted:

```bash
#!/bin/bash

# Watchdog Prometheus – executed every minute via cron
if ! pgrep -f "/-redacted-/youruser/ML_scripts/prometheus.sh" > /dev/null; then
    echo "$(date) - Prometheus not running, restarting" >> /-redacted-/youruser/ML_scripts/debug_prometheus.log
    nohup bash /-redacted-/youruser/ML_scripts/prometheus.sh >> /-redacted-/youruser/ML_scripts/debug_prometheus.log 2>&1 &
fi

# Check: if the log hasn't changed for over 5 minutes, the script may be zombie
LOG_FILE="/-redacted-/youruser/ML_scripts/debug_prometheus.log"
if [ -f "$LOG_FILE" ]; then
    last_mod=$(stat -c %Y "$LOG_FILE")
    now=$(date +%s)
    diff=$((now - last_mod))
    if [ "$diff" -gt 300 ]; then
        echo "$(date) - WARNING: log inactive for $diff seconds. Forcing restart." >> "$LOG_FILE"
        pkill -f "/-redacted-/youruser/ML_scripts/prometheus.sh"
        nohup bash /-redacted-/youruser/ML_scripts/prometheus.sh >> "$LOG_FILE" 2>&1 &
    fi
fi
```

This script is scheduled in `cron` every minute:

```cron
* * * * * /-redacted-/youruser/system-scripts/run_prometheus.sh
```

## 3. Weekly Log Cleanup

To prevent the debug log from growing indefinitely, a weekly cleanup script empties it (without deleting the file):

```bash
#!/bin/bash
# clean_prometheus_debug.sh
: > /-redacted-/youruser/ML_scripts/debug_prometheus.log
```

This is scheduled via `cron`:

```cron
0 4 * * 1 /-redacted-/youruser/system-scripts/clean_prometheus_debug.sh
```

## 4. Signal Handling

The `prometheus.sh` script handles SIGINT, SIGTERM, and SIGQUIT signals:

- `SIGINT` / `SIGTERM` → clean shutdown  
- `SIGQUIT` → forced kill and exit

```bash
trap handle_sigterm SIGINT SIGTERM
trap handle_sigquit SIGQUIT
```

## 5. Additional Notes

- If `Flame` remains always off (e.g. during summer), the script stays idle but ready to resume action.
- If a silent failure occurs (e.g. blocked log), the watchdog will detect and restart it.

---

# Block 4 – Maintenance and Diagnostics

## 1. Log Files Used

- **debug_prometheus.log**  
  - Path: `/-redacted-/youruser/ML_scripts/debug_prometheus.log`  
  - Writes approximately every 2 seconds  
  - Contains timestamps, Flame status, Modulation readings, startup messages, and detected issues  
  - Emptied weekly via `clean_prometheus_debug.sh`  

- **prometheus_success.log**  
  - Path: `/-redacted-/youruser/ML_scripts/prometheus_success.log`  
  - Records only successfully completed cycles  
  - Each entry is in JSON format with `timestamp_start`, `timestamp_end`, `total_time`, and `gas_consumption`  

- **prometheus_errors.log**  
  - Path: `/-redacted-/youruser/ML_scripts/prometheus_errors.log`  
  - Logs SSH command failures and related issues  

## 2. Recommended Manual Diagnostics

To check if the script is running:

```bash
pgrep -f prometheus.sh
```

To monitor activity in real time:

```bash
tail -f /-redacted-/youruser/ML_scripts/debug_prometheus.log
```

To view recent errors:

```bash
tail /-redacted-/youruser/ML_scripts/prometheus_errors.log
```

## 3. Manual Reset and Maintenance

In case of issues:

1. Manually kill the script:

```bash
pkill -f prometheus.sh
```

2. Restart manually:

```bash
nohup bash /-redacted-/youruser/ML_scripts/prometheus.sh >> /-redacted-/youruser/ML_scripts/debug_prometheus.log 2>&1 &
```

3. Optional debug log cleanup:

```bash
: > /-redacted-/youruser/ML_scripts/debug_prometheus.log
```

## 4. Recommended Backup

It is advisable to periodically back up the following:

- `prometheus_success.log`  
- `prometheus.sh` and `run_prometheus.sh`  
- Any `*.sh` scripts and `crontab -l` output  

## 5. Monitoring Frequency and Zombie Risk

- `run_prometheus.sh` performs a check every 60 seconds  
- Considered stable if the log updates every 2–4 seconds  
- If the log has not updated in more than 300 seconds, it is presumed to be stuck and will be restarted automatically  

## 6. Security

- The script does not access the internet except for Telegram notifications  
- All critical commands are logged  
- SSH credentials are assumed to be managed securely via key-based or direct access

> ⚠️ Ensure your Telegram bot token and SSH keys are not exposed in logs or public repositories.

---

# Block 5 – Full CRON Configuration

## 1. Active CRON Jobs

The current output of `crontab -l` is:

```cron
* * * * * /list1
0 3 * * * /list2
*/5 * * * * /list3
0 4 * * * /list4
0 9 */2 * * /list5
0 3 1 * * /list6
@reboot nohup bash /-redacted-/youruser/ML_scripts/prometheus.sh >> /-redacted-/youruser/ML_scripts/debug_prometheus.log 2>&1 &
* * * * * /-redacted-/youruser/system-scripts/run_prometheus.sh
0 4 * * 1 /-redacted-/youruser/system-scripts/clean_prometheus_debug.sh
```

> NOTE: This CRON schedule is for documentation purposes only. Replace `/-redacted-/youruser/` with your actual user path, and avoid exposing any sensitive scripts or credentials in scheduled jobs.

## 2. Entries Relevant to Prometheus

- `@reboot ... prometheus.sh`  
  Launches the Prometheus script automatically at system startup.  
  Uses `nohup` to survive shell termination.

- `* * * * * run_prometheus.sh`  
  Watchdog that checks every minute if `prometheus.sh` is active.  
  If not found, it restarts it using `nohup`.

- `0 4 * * 1 clean_prometheus_debug.sh`  
  Empties `debug_prometheus.log` every Monday at 04:00.  
  Helps avoid disk saturation due to excessive logging.

## 3. Useful Commands

To edit the active crontab:

```bash
crontab -e
```

To check current CRON jobs:

```bash
crontab -l
```

To manually trigger the watchdog:

```bash
bash /-redacted-/youruser/system-scripts/run_prometheus.sh
```

## 4. `clean_prometheus_debug.sh` Script (Full Content)

```bash
#!/bin/bash
# Empties the debug log without deleting the file
: > /-redacted-/youruser/ML_scripts/debug_prometheus.log
```

Make sure the file is executable:

```bash
chmod +x /-redacted-/youruser/system-scripts/clean_prometheus_debug.sh
```
---

# Block 6 – Architecture and Operation of the `prometheus.sh` Script

## 1. General Structure

The `prometheus.sh` script is organized into three functional blocks:

- **Block 1 – Initialization and Setup**
  - Defines global variables and customizable parameters.
  - Includes utility functions such as `try_command`, `is_number`, `send_telegram_notification`, etc.
  - Sets up logs and initializes state variables.

- **Block 2 – Calculation Functions**
  - `calculate_gas_from_modulation`: calculates the estimated gas consumption (m³) based on the average modulation and cycle duration.
  - `log_event`: stores event data in `prometheus_success.log` and sends a Telegram notification.

- **Block 3 – Cyclical Monitoring**
  - The `monitor_heating_cycle` function:
    - Alternates every 2 seconds between reading the Flame state and the Modulation value.
    - Computes gas usage only if at least one valid value has been collected and the flame turns off.
  - Includes signal handling (`SIGTERM`, `SIGQUIT`) and automatic restart of eBUSd if not active.
  - Runs automatically on system boot and in background via `nohup`.

## 2. Detection Logic

- When **Flame changes from OFF to ON**, the script records the `start_time` and starts collecting `ModulationTempDesired` values.
- When **Flame changes back to OFF**, it computes the duration and gas consumption **only if**:
  - The duration is greater than 0 seconds.
  - At least one valid modulation value was collected.
- Results are saved in the success log and sent via Telegram.

## 3. Read Frequency

- The script alternates between reading **Modulation** and **Flame** every 2 seconds.
- This results in:
  - One Modulation read every 4 seconds.
  - One Flame read every 4 seconds.
- The balanced rhythm ensures synchronized data collection without parallel processes.

## 4. Advantages of This Architecture

- **Reliability**: No parallel subprocesses → reduced risk of zombie or locked states.
- **Clarity**: Continuous detailed logging every 2 seconds.
- **Modularity**: Each function is clearly separated, testable, and documentable.
- **Resilience**: Watchdog and CRON protections guarantee recovery after faults or errors.

## 5. Expected Output

- `debug_prometheus.log`:
  - Logs every step (start, errors, flame on/off, modulation values).
- `prometheus_success.log`:
  - Stores JSON-formatted events with timestamps, duration, and estimated gas.
- Real-time Telegram notification for each completed cycle.

> ⚠️ Ensure that your Telegram bot token and chat ID, if configured in the script, are not published in the code or logs.

---

# Block 7 – Watchdog, Protections and Fallback

## Objective

Ensure that `prometheus.sh` is **always running**, using:

- Automatic startup on boot (`@reboot`)
- Watchdog every 1 minute (`run_prometheus.sh`)
- Detection of zombie/stuck script (log inactive for over 5 minutes)
- Weekly log cleanup to avoid disk saturation

## Watchdog Script – `/-redacted-/youruser/system-scripts/run_prometheus.sh`

```bash
#!/bin/bash

LOG_PATH="/-redacted-/youruser/ML_scripts/debug_prometheus.log"
SCRIPT_PATH="/-redacted-/youruser/ML_scripts/prometheus.sh"

# Check if the log has been inactive for more than 5 minutes
if [ -f "$LOG_PATH" ]; then
    last_update=$(stat -c %Y "$LOG_PATH")
    now=$(date +%s)
    diff=$((now - last_update))
    if [ "$diff" -gt 300 ]; then
        echo "$(date) - Log inactive for over 5 minutes, restarting Prometheus" >> "$LOG_PATH"
        pkill -f "$SCRIPT_PATH"
        sleep 2
    fi
fi

# Start if not already running
if ! pgrep -f "$SCRIPT_PATH" > /dev/null; then
    echo "$(date) - Prometheus not running, starting it" >> "$LOG_PATH"
    nohup bash "$SCRIPT_PATH" >> "$LOG_PATH" 2>&1 &
fi
```

## Associated CRON Jobs

```cron
# Watchdog every minute
* * * * * /-redacted-/youruser/system-scripts/run_prometheus.sh

# Startup on system boot
@reboot nohup bash /-redacted-/youruser/ML_scripts/prometheus.sh >> /-redacted-/youruser/ML_scripts/debug_prometheus.log 2>&1 &
```

## Weekly Log Cleanup

### Script `/-redacted-/youruser/system-scripts/clean_prometheus_debug.sh`

```bash
#!/bin/bash
: > /-redacted-/youruser/ML_scripts/debug_prometheus.log
```

### CRON

```cron
# Cleanup every Monday at 04:00
0 4 * * 1 /-redacted-/youruser/system-scripts/clean_prometheus_debug.sh
```

## Managed Scenarios

| Critical Case                    | Automatic Action                          |
|----------------------------------|-------------------------------------------|
| Script not running               | Watchdog starts it                        |
| Zombie script (inactive log)     | Forced restart using `pkill`              |
| System reboot                    | Automatic launch via `@reboot`            |
| Log file growing too large       | Weekly cleanup with empty file            |

## Optional Future Expansions

- Telegram notification upon forced restart  
- Separate error logging (`prometheus_errors.log`)  
- Systemd-based version instead of cron

> ⚠️ Reminder: if implementing Telegram notifications, make sure your bot token and chat ID are never exposed in public repositories.

---


## 8. Preventive Maintenance Requirements

To ensure continuous operation of the `prometheus.sh` script, the following preventive maintenance actions are recommended:

- **Weekly log check** (`debug_prometheus.log`, automated): the log is emptied every Monday at 04:00 to prevent disk space issues.
- **Automatic monitoring every minute**: the `run_prometheus.sh` script verifies that `prometheus.sh` is running and restarts it if necessary.
- **Automatic startup on every reboot**: handled via `@reboot` in the crontab.
- **Recommended manual maintenance**:
  - Every 1–2 months, check the size of `prometheus_success.log`.
  - Check `prometheus_errors.log` for recurring errors or anomalies.

These measures help ensure long-term reliability and reduce the risk of undetected failures.

---

## 9. Accuracy in Detecting Short Heating Cycles

The `prometheus.sh` script is designed to automatically detect flame ignition cycles, including short ones. However, due to alternating reads between `ModulationTempDesired` and `Flame`, there are practical limits to the minimum detection resolution.

### Sampling Frequency

- The script performs **one reading every 2 seconds**, alternating:
  - `ModulationTempDesired`
  - `Flame`
- Therefore, each parameter is read **once every 4 seconds**.

### Behavior with Micro-Cycles

| Cycle Duration (sec) | Detection Probability | Notes                                      |
|----------------------|------------------------|--------------------------------------------|
| < 4 sec              | **Very low**           | May be completely missed                   |
| 5–7 sec              | **Low**                | Detectable only if perfectly synchronized  |
| 8–12 sec             | **Medium–High**        | At least one valid read for both values    |
| > 12 sec             | **High**               | Stable and reliable detection              |

### Realistic Minimum Threshold

To consider a cycle valid for consumption calculation, the following are required:

- **At least one `Flame = on` reading**
- **At least one valid `Modulation` reading while the flame is on**
- **A following `Flame = off` reading**

This implies a **realistic minimum duration of ~8 seconds** to ensure statistical reliability and valid modulation averaging.

### Final Notes

- Cycles lasting **10–12 seconds** are consistently detected, as confirmed by recent testing.
- Cycles shorter than **6–8 seconds** may be completely missed.
- Reducing the `sleep` interval to 1 second is technically possible, but would significantly increase system load and log verbosity.
---

---

**Security Notice**  
This file has been scanned using [`leakscan.py`](./leakscan.py), a custom security tool designed to detect potential secrets, credentials, and high-risk patterns in text files.  
For more information or to contribute, refer to the script's README in this repository.

---
