# Refactoring Pipeline Tasks

## Tasks To Do:

- [ ] Implement the `--help` command with a description of the ADMIN options for pre-set cron jobs and all necessary help text.
- [ ] Make the `--admin` option necessary to unlock automatic execution functionalities (cron jobs).
- [ ] Implement a more sophisticated algorithm selection logic, considering:
    - [ ] More supported algorithms.
    - [ ] Priority-based selection logic based on data characteristics and performance.
    - [ ] Monitoring of RAM and CPU usage (`psutil`).
    - [ ] Suggestion (in logs) of lighter algorithms in case of high consumption (externally configurable).
- [ ] Move all thresholds (R², correlation, SHAP, RAM/CPU) to an external configuration file (`config_pipeline.py`).
- [ ] Implement saving prediction results to a Google Sheet (externally configured).
- [ ] Implement the management of the prediction time window (externally configurable).
- [ ] Implement prediction reliability warnings as a percentage, based on defined metrics, with an externally configurable warning threshold.
- [ ] Reorganize the code into smaller and more modular functions.
- [ ] Implement a dedicated function for loading and managing configuration from the external file.
- [ ] Restructure the main flow to handle the default interactive mode and the automatic mode (`ADMIN`).
- [ ] Enhance the use of `argparse` for comprehensive command-line option management.
- [ ] Define and implement the "weight" or priority logic for algorithms.
- [ ] Centralize the management of alerts and allow their external configuration.
- [ ] Review and enhance the Google Sheets output function.
- [ ] Add a configuration section and logic for managing the time window.
- [ ] Implement the logic to estimate prediction reliability.
- [ ] Perform thorough unit and integration tests after each phase.

## Tasks Completed:

