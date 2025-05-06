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

  **Usage:**
  ```bash
  chmod +x auto-updater.sh
  sudo ./auto-updater.sh
```

</details>
