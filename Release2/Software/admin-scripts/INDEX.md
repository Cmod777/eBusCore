# Software Index

## Update Pending: Lightweight Incremental Backup Script

The current `SaveMeImage.sh` script is highly effective and generates a complete bitwise image of the Raspberry Pi system. While this provides a full, restorable, and bootable snapshot of the entire device, it is inherently **heavy and time-consuming**, especially when run over a network. The full image includes unused space and low-level data, which can make the process slow even if the system is only partially filled.

To improve flexibility and speed, a **lightweight companion script** is planned. This future script will:

- Be designed for **faster execution**, ideal for **daily or frequent backups**.
- Focus on **user data, configuration files, logs, scripts, and critical working directories** (e.g., `~/`, `/etc/`, `/home`, `/var/log`, ML datasets, analysis results, etc.).
- Not produce a bootable image, but rather a **safe snapshot of essential data**.
- Reduce bandwidth and storage usage significantly, making it suitable for **intermediate backups** between full image captures.

> **Warning**  
> Since it will not include system-level files or boot partitions, this method **cannot recover a broken OS**. However, it will provide quick access to key files and reduce the risk of data loss.

---

### Note:
The long-term strategy is to **combine both scripts**:
- `SaveMeImage.sh` will ensure periodic **full system integrity and disaster recovery**.
- The new incremental script will offer **speed and flexibility**, acting as a **daily safety net**.

This dual-backup approach ensures **maximum reliability** while balancing resource use.

---

<details>
  <summary>SaveMeImage.sh <code>2025-05-06</code> <code>upgrade</code> <code>active</code></summary>


The original SaveMe.sh was a purely technical backup script.
It has now been fixed and upgraded to SaveMeImage.sh, which generates
a fully bootable SD-card image—making backups faster, more user-friendly,
and ready to deploy with a single write.

</details>

<details>
  <summary>auto-updater.sh <code>2025-05-06</code> <code>automation</code> <code>active</code></summary>

  A shell script for Debian‐based systems that:
  - Automatically runs `apt update` and `apt upgrade`
  - Sends Telegram notifications on success or failure
  - Logs operations and errors to separate files
  - Waits for other scripts to finish before rebooting if needed
  - Shows progress steps in the terminal

</details>

<details>
  <summary>cronwatch.sh <code>2025-05-06</code> <code>monitoring</code> <code>active</code></summary>

  A Bash script that monitors all cron jobs on Debian-based systems by checking syslog timestamps.  
  It identifies jobs that have never run or haven’t run within warning/critical thresholds, logs issues,  
  and sends Telegram notifications for delayed or missed executions.

  **Features:**
  - Aggregates user and system crontabs plus `/etc/cron.d/` entries  
  - Warns if a job hasn’t run in the last 2 hours (warning) or 6 hours (critical)  
  - Logs OK status, warnings, and errors to separate files  
  - Sends Telegram alerts on warning/critical conditions  
  - Includes notes on syslog requirements, anacron, and optional systemd timer support

</details>

<details>
  <summary>log-archiver.sh <code>2025-05-06</code> <code>archive</code> <code>active</code></summary>

  A Bash script that runs monthly to archive and compress all `.log` files from a specified directory.  
  It copies logs to an archive folder, gzips them, resets the original logs with a marker entry,  
  and sends a Telegram notification upon completion.

  **Configuration:**  
  - `TOKEN` and `CHAT_ID` for Telegram  
  - `SCRIPT_DIR` for source logs  
  - `ARCHIVE_DIR` for storing archives  
  - `LOG_FILE` for archiver actions

</details>
