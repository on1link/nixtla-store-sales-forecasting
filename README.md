# Nixtla based store sales forecast

# Conventions

## Feature experiment convention

Defined as 'model/feature_set/date' where:

- Feature set is a human readable summarize set of features, e.g. 'v3_baseline' or 'v1_pricing_calendar' or 'baseline_oil'

## Definition of Done

Project complete when:

1. **Kaggle submission** — public leaderboard RMSLE below top-25% threshold
2. **Full-series coverage** — all 1,782 series forecasted, not 5-series subset
3. **Reproducible pipeline** — single config-driven `main.py` run produces submission CSV end-to-end
4. **Model comparison documented** — statistical vs neural vs gradient boosting RMSLE comparison table with CV results
5. **Experiment tracking live** — all runs logged in MLflow with hyperparams, metrics, and registered best models
6. **Tests pass** — unit tests for data, features, and evaluation modules
7. **Deployable** — chosen deployment mode (API or batch) running with health check

## Deliverables

| Artifact | Location | Description |
| ---------- | ---------- | ------------- |
| Submission CSV | `submissions/` | Kaggle-format predictions on `test.csv` |
| Trained models | MLflow Model Registry | Best model per series, tagged staging/production |
| Experiment logs | MLflow tracking server | All runs with metrics, params, artifacts |
| Comparison table | `reports/model_comparison.md` | RMSLE breakdown: statistical vs neural vs GB |
| Config file | `config.yaml` | Model params, data paths, feature toggles |
| Python pipeline | `src/data.py`, `src/features.py`, `src/models.py`, `main.py` | Modular forecasting pipeline |
| Test suite | `tests/` | Unit tests for data, features, evaluation |
| API/Batch service | `deploy/` | Forecasting service with health check |

## TODO

### 1. Experiment Tracking (MLflow)

- [ ] Set up MLflow tracking server (local or remote)
- [ ] Log all model × feature × series CV runs with metrics (MAE, RMSE, RMSLE)
- [ ] Track hyperparameters and exogenous variable combos per run
- [ ] Query best model per `unique_id` by CV metric
- [ ] Model registry: store winning model per series for retraining

### 2. Critical Fixes & Repo Hygiene

- [x] Fix evaluation merge producing cartesian product (1,280 rows from 80 test rows)
- [x] Add `.gitignore` entries for `lightning_logs/`, `*.png`, `.ipynb_checkpoints/`
- [x] Use RMSLE (Kaggle competition metric) instead of MAE/RMSE

### 3. Data & Feature Engineering

- [ ] Handle 31.3% zero-sales entries (intermittent demand strategy)
- [ ] Improve oil price missing value imputation (currently ffill/bfill)
- [ ] Incorporate holidays.csv and transactions.csv as exogenous variables
- [ ] Add promotion (`onpromotion`) as exogenous regressor
- [ ] Engineer store metadata features (city, state, type, cluster from stores.csv)
- [ ] Scale to all 1,782 time series (currently using 5 subset categories)

### 4. Modeling — Nixtla (Statistical + Neural)

- [ ] Add exogenous variables to NeuralForecast models (oil, promotions)
- [ ] Tune NeuralForecast models (LSTM/GRU/RNN) — increase `max_steps`, grid search hyperparameters
- [x] Try NHITS and PatchTST from NeuralForecast
- [ ] Implement hierarchical forecasting: store-level → family-level reconciliation
- [ ] Ensemble top-performing statistical + neural models

### 5. Modeling — Gradient Boosting Ensemble (Kaggle Winning Approach)

#### Architecture

Hybrid of two forecasting strategies:

1. **Recursive Global Ensemble** — weighted blend of LightGBM (35%), CatBoost (40%), XGBoost (25%). Uses log-transformed target and weighted training emphasizing recent observations.
2. **Direct Multi-Horizon Forecasting** — 16 separate direct models (one per forecast horizon day).
3. **Final prediction** — 60% recursive ensemble + 40% direct multi-horizon ensemble.

#### Feature Engineering

- [ ] Time features: day of week, week of year, month, year, day of year, month-end flags, Fourier seasonal terms
- [ ] Lag features: sales lags (1, 7, 14, 28 days), rolling mean/std (7-day, 28-day windows)
- [ ] Promotion features: promotion lags, promotion rolling averages
- [ ] Target encoding: store avg sales, family avg sales, store-family avg sales
- [ ] External data: oil prices, store metadata, transactions, holiday/event signals

#### Models

- [ ] LightGBM with GPU-accelerated training
- [ ] CatBoost with GPU-accelerated training
- [ ] XGBoost with GPU-accelerated training
- [ ] Weighted recursive ensemble (LGB 35% / CB 40% / XGB 25%)
- [ ] Direct multi-horizon models (16 independent horizon models)
- [ ] Final hybrid blend (60% recursive / 40% direct)
- [ ] Log target transformation + recent-observation weighted learning

### 6. Evaluation & Submission

- [ ] Cross-validate on full dataset (currently 3 folds, 5 series)
- [ ] Benchmark neural models against statistical baselines on same splits
- [ ] Benchmark gradient boosting ensemble against all other approaches
- [ ] Generate predictions on `test.csv` for Kaggle submission

### 7. Pipeline & Code Quality

- [ ] Refactor notebook into modular Python pipeline (`main.py` is stub)
- [ ] Add CLI interface for running forecasts
- [ ] Implement unit tests for data processing and evaluation

### 8. Deployment

- [ ] Build reproducible training pipeline (config-driven)
- [ ] Add data versioning (DVC or similar)
- [ ] Deploy forecasting service (API or batch)
