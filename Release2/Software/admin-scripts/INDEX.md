Software Index

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
