# Refactoring Pipeline Tasks

## Tasks To Do:

- [ ] Implement the `--help` command with a description of the ADMIN options for pre-set cron jobs and all necessary help text.
- [ ] Make the `--admin` option necessary to unlock automatic execution functionalities (cron jobs).
- [x] ![Implemented in v1.3](https://img.shields.io/badge/Implemented%20in-v1.3-brightgreen)
 Implement a more sophisticated algorithm selection logic, considering:
    - [x] ![Implemented in v1.3](https://img.shields.io/badge/Implemented%20in-v1.3-brightgreen)
 More supported algorithms.
    - [x] ![Implemented in v1.3](https://img.shields.io/badge/Implemented%20in-v1.3-brightgreen)
 Priority-based selection logic based on data characteristics and performance.
    - [x] ![Implemented in v1.3](https://img.shields.io/badge/Implemented%20in-v1.3-brightgreen)
 Monitoring of RAM and CPU usage (`psutil`).
    - [x] ![Implemented in v1.3](https://img.shields.io/badge/Implemented%20in-v1.3-brightgreen)
 Suggestion (in logs) of lighter algorithms in case of high consumption (externally configurable).
- [ ] Move all thresholds (R², correlation, SHAP, RAM/CPU) to an external configuration file (`config_pipeline.py`).
- [ ] Implement saving prediction results to a Google Sheet (externally configured).
- [ ] Implement the management of the prediction time window (externally configurable).
- [ ] Implement prediction reliability warnings as a percentage, based on defined metrics, with an externally configurable warning threshold.
- [x] ![Implemented in v1.3](https://img.shields.io/badge/Implemented%20in-v1.3-brightgreen)
 Reorganize the code into smaller and more modular functions.
- [ ] Implement a dedicated function for loading and managing configuration from the external file.
- [ ] Restructure the main flow to handle the default interactive mode and the automatic mode (`ADMIN`).
- [ ] Enhance the use of `argparse` for comprehensive command-line option management.
- [ ] Define and implement the "weight" or priority logic for algorithms.
- [ ] Centralize the management of alerts and allow their external configuration.
- [ ] Review and enhance the Google Sheets output function.
- [ ] Add a configuration section and logic for managing the time window.
- [ ] Implement the logic to estimate prediction reliability.
- [ ] Perform thorough unit and integration tests after each phase.

- [ ] Ensure robust exception handling in potentially problematic code blocks (external connections, data manipulation, model training).
- [ ] Implement intelligent retry or fallback mechanisms where applicable.
- [ ] Validate user inputs carefully to prevent errors and unexpected behavior.
- [ ] Implement basic data integrity checks (missing values, incorrect data types) and provide handling options.
- [ ] Consider efficient data loading strategies (batch processing, generators) for large datasets.
- [ ] Explore training optimization techniques (GPU usage, parallelization) for complex models or large datasets.
- [ ] Consider future scalability needs when designing the code.
- [ ] Follow clear and consistent naming conventions for variables, functions, and classes.
- [ ] Add clear comments to explain complex logic and document functions (docstrings).
- [ ] Separate code responsibilities into distinct modules or classes (configuration, data loading, training, output).
- [ ] Avoid code duplication by creating reusable functions or classes (DRY principle).
- [ ] Structure the code to facilitate writing unit tests and integration tests.
- [ ] Create automated tests to ensure future changes don't break existing functionality.
- [ ] Ensure secure handling of credentials for accessing Google Sheets or other services.
- [ ] Consider injection prevention principles if integrating external, uncontrolled inputs in the future.
- [ ] If model training evolves, implement a versioning system to track used models and parameters.
- [ ] Recording model performance over time to detect drift or the need for retraining.
- [ ] Adding a dashboard or visualizations to facilitate the interpretation of results and performance.

## Tasks Completed:

