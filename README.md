# End-to-End Industrial Predictive Maintenance System

A multi-disciplinary engineering project combining **Statistical Process Control (SPC)**, **Signal Processing (FFT)**, **Machine Learning (LightGBM)**, and **Business Intelligence (Power BI)** to intercept catastrophic manufacturing asset failures before they occur.

## 📌 Project Overview
Unplanned machine downtime costs manufacturing operations billions annually. This project builds a reliable, proactive pipeline to predict milling machine failures. By transforming raw, noisy time-series vibration data into distinct frequency domain features, the final model achieved a **100% Recall rate**, capturing every single breakdown on hidden test data without a single false alarm.

---

## 🛠️ The Architecture Pipeline

### 1. Financial & Statistical Modeling (Excel)
* Calculated the baseline operational costs and established that unmitigated tool failure translates to a simulated **$305.1M** operational risk.
* Applied Statistical Process Control to establish an Upper Control Limit ($UCL$) at $+3\sigma$ for safe thermal boundaries.

### 2. Relational Storage & Exploratory Analysis (SQL)
* Structured an SQLite relational database (`factory_vault.db`) to hold 10,000 telemetry entries.
* Developed optimized queries using **Common Table Expressions (CTEs)** to isolate and group high-risk temperature excursions across three machinery variants (L, M, H).

### 3. Signal Processing & Feature Engineering (SciPy & FFT)
* Realized that thermal limits lag behind actual physical micro-fractures.
* Implemented a **Fast Fourier Transform (FFT)** algorithm to convert raw, time-varying vibration waveforms into frequency-domain spectrum arrays.
* Extracted structural health markers (`FFT_Max_Amplitude` and `FFT_Dominant_Peak`), providing explicit indicators of bearing degradation.

### 4. Predictive Machine Learning Machine (LightGBM)
* Trained a **LightGBM Classifier** using an 80/20 stratified split to protect against severe class imbalance (only 3.3% of entries represent failures).
* **Results:** Upgrading the input feature space with our engineered FFT metrics caused the model's prediction capabilities to jump from an initial **65% recall to a perfect 100% precision and recall**.

### 5. Live Dashboard & Executive Reporting (Power BI)
* Engineered a live telemetry streaming script to simulate an industrial control room interface.
* Exported the core insights into a professional **Power BI Dashboard** that maps:
  * Overall financial exposure card (**$305.10M**).
  * Real-time machine health state via conditional traffic-light formatting.
  * Mechanical stress tracking utilizing an asset vibration speedometer gauge.

---

## 📂 Repository Contents
* `create_database.py`: Initializes the relational SQLite framework.
* `run_queries.py`: Processes analytics queries using advanced SQL CTEs.
* `build_advanced_features.py`: Applies Fast Fourier Transforms to extract spectral peaks.
* `train_model.py`: Executes the LightGBM classifier training pipeline.
* `live_monitor.py`: Simulates a streaming real-time control room warning system.
* `ai4i2020.xlsx`: The original data exploration sheet containing statistical process boundaries.
* `machine_health_status_indicator.pbix`: The complete visual Power BI architecture layout.

---

## 📈 Final Model Performance Metrics
```text
=== UPGRADED ML MODEL PERFORMANCE ===
Overall Model Accuracy: 100.00%

Detailed Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00      1932
           1       1.00      1.00      1.00        68

    accuracy                           1.00      2000