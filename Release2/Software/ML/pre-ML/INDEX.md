## Overview

The old scripts in this repository have been removed. They were originally built for testing and experimentation, but over time we've found a much better and cleaner solution. This new version includes just **two core scripts** that together manage the entire data pipeline in a simplified and optimized way.

We no longer rely on complex permission chains, separate read/write handlers, or unstable API usage. Everything is now centralized, faster, and easier to maintain.

---

## Script 1 – `importDB.py`

This script downloads a full copy of the Google Sheets database and saves it as a local `.csv` file.

<details>
<summary><strong>What does it do?</strong></summary>

- Connects once to Google Sheets using a single authentication step.
- Automatically fetches the full sheet content.
- Saves the raw database locally as `db.csv`.

In previous implementations, we had separate scripts for reading and writing, each requiring its own login flow, scope settings, and error handling. This caused problems with token refresh, cell limits, quota exhaustion, and fragile automation.

With `importDB.py`, **all that is gone**. This script logs in **only to read**, and dumps the entire sheet content at once.

</details>

<details>
<summary><strong>Why use a local copy?</strong></summary>

- **No API latency**: working locally is much faster and smoother than reading from Google each time.
- **Stability**: your local file can be versioned, archived, compared over time.
- **Offline access**: scripts can work without internet once the file is saved.
- **Longevity**: the Google copy can be trimmed or cleaned periodically, while the local file stays permanent.

</details>

---

## Script 2 – `extractor.py`

This script reads the local database (`db.csv`) and applies transformation rules from a local configuration file (`keys.yaml`) to produce a clean, structured output for machine learning.

<details>
<summary><strong>What does it do?</strong></summary>

- Loads the raw database (`db.csv`)
- Loads interpretation rules from `keys.yaml`
- Applies preprocessing, type casting, and column-level logic
- Applies specific interpolation rules per column
- Outputs a cleaned file: `db_clean.csv`

This clean dataset is the foundation for all subsequent ML or analytics steps. It contains only valid, interpreted, numeric-ready data, aligned with your defined rules.

</details>

---

## Summary

| Script         | Purpose                                               |
|----------------|-------------------------------------------------------|
| `importdb.py`  | Import and save a full local copy of the Google Sheet |
| `extractor.py` | Process and clean the local copy using `keys.yaml` |

This setup removes API dependency during processing, speeds up development, and ensures a consistent offline-ready workflow.

---

## Requirements

Install these Python packages:

```bash
pip install gspread oauth2client pandas pyyaml numpy
```

You also need a Google service account and the `creds.json` file placed in the root directory. This is required **only** by `importDB.py`, and only once at first use.

---

## System Purpose and Redundancy Strategy

This data pipeline was designed to ensure reliable, fast, and redundant access to a structured version of your database originally stored on Google Sheets. The system includes:

- One script to fetch the full Google Sheet and save a local copy (`importDB.py`)
- One script to clean, format, and prepare the data using custom parsing rules (`extractor.py`)

These scripts form the core of a **resilient, reproducible preprocessing workflow** intended for data science, machine learning, and analytics.

---

## Python Requirements

Make sure the following Python modules are installed:

```bash
pip install gspread oauth2client pandas numpy pyyaml
```

Also ensure:
- A valid `creds.json` file is in the project root for Google Sheets access.
- Python 3.7 or later is recommended.

---

## Automation (Crontab)

> **Note**: This workflow is not complete without scheduling.

Both `importDB.py` and `extractor.py` should be configured to run every 30 minutes using `crontab`, to ensure:
- The local copy is refreshed with any updates from Google Sheets
- The cleaned dataset (`db_clean.csv`) is always up to date and ready for downstream processes

Example `crontab` entry:

```cron
*/30 * * * * /usr/bin/python3 /home/youruser/scripts/importdb.py
*/30 * * * * /usr/bin/python3 /home/youruser/scripts/extractor.py
```

Make sure the paths and Python interpreter are correct for your environment.

---

## Planned Extension: Data Replication with rsync

A third script will be introduced using `rsync` to replicate the key output files (`db.csv` and `db_clean.csv`) to a secondary machine.

This will provide **redundant layers of storage**:
1. The original Google Sheet (cloud)
2. The local copy on the primary machine
3. A synchronized clone on a secondary local machine

This design minimizes the risk of data loss and ensures resilience across hardware or network failures.

---

## License

All scripts in this repository are provided under:

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) + custom (see LICENSE.md)**

You may copy, use, and adapt the software for **non-commercial purposes only**, with proper credit to the original author (Cmod777). Commercial redistribution, resale, or inclusion in proprietary platforms is strictly prohibited.
