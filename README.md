# Nixtla based store sales forecast

## TODO

### 1. Critical Fixes & Repo Hygiene

- [x] Fix evaluation merge producing cartesian product (1,280 rows from 80 test rows)
- [x] Add `.gitignore` entries for `lightning_logs/`, `*.png`, `.ipynb_checkpoints/`
- [x] Use RMSLE (Kaggle competition metric) instead of MAE/RMSE

### 2. Data & Feature Engineering

- [ ] Handle 31.3% zero-sales entries (intermittent demand strategy)
- [ ] Improve oil price missing value imputation (currently ffill/bfill)
- [ ] Incorporate holidays.csv and transactions.csv as exogenous variables
- [ ] Add promotion (`onpromotion`) as exogenous regressor
- [ ] Engineer store metadata features (city, state, type, cluster from stores.csv)
- [ ] Scale to all 1,782 time series (currently using 5 subset categories)

### 3. Modeling

- [ ] Add exogenous variables to NeuralForecast models (oil, promotions)
- [ ] Tune NeuralForecast models (LSTM/GRU/RNN) — increase `max_steps`, grid search hyperparameters
- [x] Try NHITS and PatchTST from NeuralForecast
- [ ] Implement hierarchical forecasting: store-level → family-level reconciliation
- [ ] Ensemble top-performing statistical + neural models

### 4. Evaluation & Submission

- [ ] Cross-validate on full dataset (currently 3 folds, 5 series)
- [ ] Benchmark neural models against statistical baselines on same splits
- [ ] Generate predictions on `test.csv` for Kaggle submission

### 5. Pipeline & Code Quality

- [ ] Refactor notebook into modular Python pipeline (`main.py` is stub)
- [ ] Add MLflow or experiment tracking for model comparisons
- [ ] Add CLI interface for running forecasts
- [ ] Implement unit tests for data processing and evaluation

### 6. Deployment

- [ ] Build reproducible training pipeline (config-driven)
- [ ] Add data versioning (DVC or similar)
- [ ] Deploy forecasting service (API or batch)
