# JALNETRA — Backend, AI & Offline Implementation Status

## Purpose

This document records the **backend work actually completed and tested in VS Code so far**.

Future AI ideas are explicitly marked as **NOT IMPLEMENTED YET**.

---

## 1. Backend Stack

- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite/local database
- Pydantic / pydantic-settings
- APScheduler
- Pandas
- XGBoost
- scikit-learn
- joblib

Verified environment:

```text
XGBoost: 3.3.0
scikit-learn: 1.9.0
joblib: 1.5.3
```

---

## 2. Current AI Model — XGBoost

The main trained model is:

```text
app/ml/models/flood_model.pkl
```

Verified type:

```text
xgboost.sklearn.XGBRegressor
```

Purpose:

> Predict localized flood/water depth in centimeters for each zone.

The model is loaded by:

```text
app/ml/model_loader.py
```

Additional model files:

```text
encoders.pkl
feature_columns.pkl
```

Verified encoder keys:

```text
land_cover
soil_type
```

Land-cover classes:

```text
Agricultural
Desert
Forest
Urban
Water Body
```

Soil classes:

```text
Clay
Loam
Peat
Sandy
Silt
```

---

## 3. AI Feature Pipeline

Implemented in:

```text
app/ml/feature_builder.py
```

Current model features include:

```text
latitude
longitude
rainfall_mm
temperature_c
humidity_percent
river_discharge_m³_s
water_level_m
elevation_m
land_cover
soil_type
population_density
infrastructure
historical_floods
rainfall_discharge
rainfall_waterlevel
terrain_risk
population_risk
weather_severity
infra_risk
```

The feature builder combines:

```text
weather
+
zone data
+
hydrology calculations
```

before sending features to XGBoost.

A `weather_override` option was also implemented and successfully tested.

---

## 4. Weather Integration

Implemented in:

```text
app/services/weather_service.py
```

Provider:

```text
Open-Meteo
```

Configured endpoint:

```text
https://api.open-meteo.com/v1/forecast
```

Configured location:

```text
Latitude: 9.98
Longitude: 76.28
```

Weather inputs currently include:

```text
temperature
relative humidity
precipitation
```

Hydrology inputs are derived through:

```text
app/services/hydrology_inputs.py
```

---

## 5. Weather Caching

Open-Meteo hourly data is cached through:

```text
app/services/cache_service.py
```

Current cache key:

```text
openmeteo:hourly
```

The cache reduces repeated external weather requests.

---

## 6. Hydrology Layer

Implemented in:

```text
app/services/hydrology_service.py
```

This is **physics/rule based, not AI**.

Current calculations:

```text
runoff
soil_saturation
drainage_efficiency
canal_overflow
flow_velocity
storage_capacity
flood_potential
```

JalNetra therefore uses a:

> **Hybrid AI + physics-based architecture.**

---

## 7. Current Prediction Pipeline

```text
Weather
   ↓
Feature Builder
   ↓
Hydrology Calculations
   ↓
Feature Encoding
   ↓
XGBoost AI
   ↓
Predicted Water Depth
   ↓
Risk Engine
   ↓
Trend + Citizen Reports
   ↓
Alert Engine
   ↓
Zone Result
```

Main components:

```text
app/ml/predictor.py
app/services/prediction_service.py
```

---

## 8. Risk Engine

Current risk thresholds have been tested:

```text
0 – 9.99 cm       → SAFE
10 – 24.99 cm     → WATCH
25 – 49.99 cm     → HIGH
50+ cm            → SEVERE
```

This is currently **rule-based**, not a separate ML classifier.

---

## 9. Citizen Reports

Implemented through:

```text
app/api/reports.py
app/services/report_service.py
app/models/report.py
```

Report fields:

```text
id
zone
description
severity
latitude
longitude
depth_cm
road_blocked
created_at
```

Citizen reports are already incorporated into the alert/trend logic.

---

## 10. Trend Detection

Recent water-depth reports are compared to determine:

```text
rising
falling
steady
```

Current rule:

```text
latest - previous >= 5 cm
    → rising

latest - previous <= -5 cm
    → falling

otherwise
    → steady
```

This was successfully tested using Kaloor:

```text
20 cm → 30 cm
```

Result:

```text
trend: rising
```

Trend detection is currently **algorithmic, not ML**.

---

## 11. Alert Intelligence

The alert system combines:

```text
predicted depth
risk
risk level
water-level trend
recent citizen reports
blocked-road reports
```

A tested Kaloor scenario produced:

```text
alertLevel: high
alertTriggered: True
recentReports: 6
blockedRoadReports: 2
trend: rising
```

Alert reasons included:

```text
Recent citizen reports indicate rising water levels.
6 recent citizen reports were received.
2 recent report(s) indicate road blockage.
```

This is currently rule-based intelligence.

---

# 12. Nowcast Endpoint

Main endpoint:

```text
GET /nowcast
```

Supported forecast offsets:

```text
0
30
60
90
120
```

Invalid offset:

```text
45
```

returns:

```text
400 Bad Request
```

Rainfall validation was tested:

```text
rain=121 → 400 Bad Request
rain=-1  → 400 Bad Request
```

---

## 13. Zone Response

The nowcast response currently contains:

```text
id
name
lat
lng
depthCm
risk
level
recommendation
population
trend
confidence
alertLevel
alertTriggered
alertReasons
recentReports
blockedRoadReports
```

This combines ML prediction, hydrology, reports, trend analysis and alerts.

---

# 14. Two-Hour Forecast

JalNetra uses a rolling forecast window:

```text
0 min
30 min
60 min
90 min
120 min
```

This provides a **2-hour flood outlook**.

---

# 15. Automatic 30-Minute Synchronization

Implemented with:

```text
APScheduler
AsyncIOScheduler
```

The scheduler runs every:

```text
30 minutes
```

A synchronization is also performed when the backend starts.

Verified startup output:

```text
Loading AI Model...
AI Model Loaded Successfully.
Scheduled sync completed: 772.56 ms
JalNetra automatic sync started (every 30 minutes).
Application startup complete.
```

Therefore automatic synchronization is confirmed working.

---

# 16. Emergency Synchronization

An emergency refresh can bypass the normal 30-minute schedule.

Verified:

```text
status: live
syncType: emergency
processingTimeMs: 31.33
```

The target maximum update time is:

```text
2 minutes
```

The measured emergency synchronization time is far below that limit.

---

# 17. Offline-First Architecture

The intended behavior is:

### When internet is available

```text
Internet
   ↓
Latest weather
   ↓
AI + hydrology processing
   ↓
2-hour forecast
   ↓
Local snapshot
```

### When internet disappears

```text
No live weather request
       ↓
Load last successful snapshot
       ↓
Continue serving forecast
```

The system does **not** claim to create new live weather information while completely offline.

Instead:

> The latest successfully synchronized AI forecast remains locally available during network loss.

---

# 18. Offline Test

Offline retrieval was successfully verified:

```text
status         : offline
syncType       : emergency
generatedAt    : 2026-08-18T23:29:20.601216+00:00
dataAgeSeconds : 23.04
```

This confirms the backend can serve the locally stored forecast without performing a new live synchronization.

---

# 19. Synchronization Architecture

```text
             ONLINE
                │
                ▼
       Weather synchronization
                │
                ▼
          AI prediction
                │
                ▼
       2-hour forecast package
                │
                ▼
        Local snapshot/cache
                │
       ┌────────┴────────┐
       ▼                 ▼
    ONLINE             OFFLINE
       │                 │
  refresh every       use latest
  30 minutes          snapshot
       │                 │
       └────────┬────────┘
                ▼
         EMERGENCY REFRESH
```

---

# 20. Measured Performance

```text
Scheduled synchronization:
~772.56 ms

Emergency synchronization:
~31.33 ms

Maximum allowed update time:
2 minutes
```

Current measured performance is comfortably within the requirement.

---

# 21. What Is Actually AI?

## Implemented AI

### XGBoost

Used for:

```text
Localized flood/water-depth prediction
```

---

## Supporting but non-AI components

### Physics based

```text
HydrologyService
```

### Rule based

```text
RiskService
Trend detection
AlertService
Validation
```

### External data

```text
Open-Meteo
```

### Infrastructure

```text
FastAPI
SQLAlchemy
SQLite
APScheduler
Local cache/snapshot
```

When pitching:

> **JalNetra combines XGBoost machine learning with physics-based hydrology, weather data and citizen observations.**

Do not claim every component is AI.

---

# 22. Model Compatibility Warnings

The current model files were created using older package versions.

Observed scikit-learn warning:

```text
Model created with scikit-learn 1.6.1
Current environment: 1.9.0
```

XGBoost also reports a serialized-model compatibility warning.

The model currently loads and predictions work.

Future maintenance should re-export/re-save the model using a compatible supported format/version.

Do not unnecessarily replace the working model during current feature development.

---

# 23. Backend Components Relevant to Current Work

```text
app/
├── api/
│   ├── alerts.py
│   ├── analytics.py
│   ├── climatology.py
│   ├── dashboard.py
│   ├── explain.py
│   ├── forecast.py
│   ├── health.py
│   ├── nowcast.py
│   └── reports.py
│
├── ml/
│   ├── feature_builder.py
│   ├── model_loader.py
│   ├── predictor.py
│   ├── preprocess.py
│   ├── train.py
│   └── models/
│
├── services/
│   ├── alert_service.py
│   ├── cache_service.py
│   ├── forecast_service.py
│   ├── hydrology_inputs.py
│   ├── hydrology_service.py
│   ├── prediction_service.py
│   ├── report_service.py
│   ├── risk_service.py
│   ├── trend_service.py
│   ├── weather_service.py
│   └── zone_service.py
│
├── models/
├── schemas/
├── database/
├── core/
└── main.py
```

---

# 24. Tests Already Passed

```text
[PASS] Nowcast endpoint responds
[PASS] Zones returned
[PASS] Zone contains id
[PASS] Zone contains name
[PASS] Zone contains lat
[PASS] Zone contains lng
[PASS] Zone contains depthCm
[PASS] Zone contains risk
[PASS] Zone contains level
[PASS] Zone contains recommendation
[PASS] Zone contains population
[PASS] Zone contains trend
[PASS] Zone contains confidence
[PASS] Zone contains alertLevel
[PASS] Zone contains alertTriggered
[PASS] Zone contains alertReasons
[PASS] Zone contains recentReports
[PASS] Zone contains blockedRoadReports

[PASS] Risk 0cm -> safe
[PASS] Risk 9.99cm -> safe
[PASS] Risk 10cm -> watch
[PASS] Risk 24.99cm -> watch
[PASS] Risk 25cm -> high
[PASS] Risk 49.99cm -> high
[PASS] Risk 50cm -> severe

[PASS] Rainfall > 120 rejected
[PASS] Negative rainfall rejected
[PASS] Invalid offset rejected
[PASS] Offset 0 accepted
[PASS] Offset 30 accepted
[PASS] Offset 60 accepted
[PASS] Offset 90 accepted
[PASS] Offset 120 accepted

[PASS] Reports endpoint responds
[PASS] Reports are returned
[PASS] Recent reports endpoint responds
```

---

# 25. Future AI — NOT IMPLEMENTED YET

These are proposed next steps and must **not** be presented as completed.

## AI Citizen Report Anomaly Detection

Possible model:

```text
Isolation Forest
```

Potential features:

```text
reported depth
predicted depth
depth difference
depth change
rainfall
time between reports
nearby-zone depth
report frequency
severity
road blocked
```

Potential output:

```text
anomaly score
is_anomaly
```

---

## Citizen Report Reliability AI

Potential signals:

```text
temporal consistency
spatial consistency
AI prediction agreement
depth consistency
severity consistency
duplicate detection
road-blockage evidence
```

Potential output:

```text
report confidence
evidence level
```

---

## Temporal Flood Forecasting

Possible future approach:

```text
XGBoost + lag features
```

Later alternatives:

```text
LSTM
Temporal CNN
Transformer
```

---

## AI Risk Classifier

Possible future model:

```text
XGBoost Classifier
```

for:

```text
SAFE
WATCH
HIGH
SEVERE
```

The existing threshold-based risk system should remain as a safety fallback.

---

## Spatial Flood Propagation

Long-term possibility:

```text
Graph-based / GNN model
```

to learn how flooding propagates between neighboring zones.

---

# 26. Current Architecture Summary

```text
                  JALNETRA
                     │
        ┌────────────┴────────────┐
        │                         │
   WEATHER DATA              CITIZEN DATA
        │                         │
        ▼                         ▼
   HYDROLOGY                REPORT DATABASE
        │                         │
        ▼                         ▼
 FEATURE BUILDER           TREND / REPORT LOGIC
        │                         │
        ▼                         │
    XGBOOST AI                   │
        │                         │
        └────────────┬────────────┘
                     ▼
                RISK ENGINE
                     │
                     ▼
                ALERT ENGINE
                     │
                     ▼
             2-HOUR FORECAST
                     │
              ┌──────┴──────┐
              ▼             ▼
           ONLINE         OFFLINE
              │             │
        30-min sync    Last snapshot
              │             │
              └──────┬──────┘
                     ▼
                 FRONTEND
```

---

# 27. Current Completion State

### COMPLETED

- [x] FastAPI backend
- [x] XGBoost flood-depth prediction
- [x] ML feature pipeline
- [x] Weather integration
- [x] Weather caching
- [x] Physics-based hydrology
- [x] Zone predictions
- [x] Risk classification
- [x] Citizen reports
- [x] Trend detection
- [x] Alert intelligence
- [x] Input validation
- [x] 2-hour forecast window
- [x] 30-minute automatic synchronization
- [x] Emergency synchronization
- [x] Local forecast snapshot
- [x] Offline snapshot retrieval
- [x] Backend validation tests

### NEXT AI DEVELOPMENT

- [ ] Citizen-report anomaly detection
- [ ] Citizen-report reliability/evidence scoring
- [ ] Temporal flood forecasting
- [ ] Optional ML risk classifier
- [ ] Future spatial flood propagation model

---

## Final Project Statement

> **JalNetra is currently a hybrid AI-powered urban flood intelligence backend that combines XGBoost-based water-depth prediction, physics-based hydrology, live weather data, citizen observations, trend analysis and alert logic. It synchronizes a rolling two-hour forecast every 30 minutes, supports immediate emergency refreshes, and retains the latest successful forecast locally for offline operation.**

**Current backend foundation and offline synchronization are complete. The next AI phase is citizen-report anomaly detection and evidence intelligence.**
