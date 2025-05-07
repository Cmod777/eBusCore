# MLpred2.py Overview

**Date:** 2025‑05‑07  
**Tags:** active, to‑implement, monitoring, machine‑learning

<details>
<summary><strong>Purpose</strong></summary>

This script automates end‑to‑end forecasting of thermal comfort indices for three zones (salotto, camera, bagno) in a smart home. It:

- Extracts raw sensor & environmental data from Google Sheets  
- Preprocesses and aggregates features (internal/external temperature, humidity, energy, device states, etc.)  
- Trains a RandomForest model per zone  
- Predicts comfort indices 12 hours ahead  
- Logs results, writes outputs back to Google Sheets, and sends Telegram alerts  
- Monitors forecast errors and triggers retraining when performance degrades  

</details>

<details>
<summary><strong>Key Functions</strong></summary>

1. **carica_fogli()**: Connects to Google Sheets, loads or creates worksheets  
2. **get_codici_utili()**: Reads legenda to select feature columns dynamically  
3. **carica_dati()**: Converts raw values, timestamp indexing, cleans and filters features  
4. **ottimizza_random_forest()**: Hyperparameter grid‑search (n_estimators, max_depth)  
5. **train_and_predict()**: Aggregates last N samples, predicts comfort index, computes MAE/RMSE, alerts  
6. **deve_riaddestrare()**: Checks time‑based and error‑threshold conditions for retraining  
7. **riaddestra_modelli()**: Retrains and caches models for each zone  
8. **scrivi_output() / scrivi_preml2()**: Writes forecasts and error logs back to Sheets  
9. **pulisci_preml2()**: Trims historical error log sheet for performance  

</details>

<details>
<summary><strong>Reliability Index</strong></summary>

| Aspect                    | Status                                     |
|---------------------------|--------------------------------------------|
| Pipeline robustness       | ★★★★☆ (automated extraction → prediction)  |
| Logging & monitoring      | ★★★★★ (INFO/ERROR logs + Telegram alerts)  |
| Retraining mechanism      | ★★★★☆ (time & error‑based)                 |
| Feature coverage          | ★★★★☆ (60+ dynamic signals)                |
| Over‑fit risk             | ★★★☆☆ (batch RF shows MAE≈0 on training)    |

Overall: **Production‑ready** for monitoring & alerting. **Caution** if used for autonomous control.

</details>

<details>
<summary><strong>How to Use</strong></summary>

1. Set your credentials JSON at `CREDS_PATH` and ensure Sheets exist.  
2. Adjust config at top (error thresholds, window size, retrain frequency).  
3. Grant execution rights: `chmod +x MLpred2.py`.  
4. Run manually or schedule via cron (e.g., hourly).  
5. Review `ML_output` and `preML2` sheets for forecasts & error history.  
6. Monitor `mlpred2.log` / `mlpred2.error.log` for diagnostics.  

</details>

<details>
<summary><strong>Future Improvements</strong></summary>

- **Online learning**: replace batch RF with a `.partial_fit`‑capable regressor (SGD, PassiveAggressive) for real‑time updates  
- **Advanced features**: add rolling trends, standard deviations, time‑of‑day encoding  
- **Validation**: implement time‑series cross‑validation hold‑out to estimate out‑of‑sample error  
- **Adaptive thresholds**: tune `ERRORE_TRIGGER_RMSE` dynamically based on seasonality  
- **Alerting enhancements**: integrate Grafana or dashboard for visual monitoring  

</details>
