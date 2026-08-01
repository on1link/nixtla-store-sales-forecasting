# Nixtla based store sales forecast

## TODO

### Data & Feature Engineering
- [ ] Scale to all 1,782 time series (currently using 5 subset categories)
- [ ] Handle 31.3% zero-sales entries (intermittent demand strategy)
- [ ] Incorporate holidays.csv and transactions.csv as exogenous variables
- [ ] Add promotion (`onpromotion`) as exogenous regressor
- [ ] Improve oil price missing value imputation (currently ffill/bfill)
- [ ] Engineer store metadata features (city, state, type, cluster from stores.csv)

### Modeling
- [ ] Tune NeuralForecast models (LSTM/GRU/RNN) — increase `max_steps`, grid search hyperparameters
- [ ] Try NHITS and PatchTST from NeuralForecast
- [ ] Add exogenous variables to NeuralForecast models (oil, promotions)
- [ ] Implement hierarchical forecasting: store-level → family-level reconciliation
- [ ] Ensemble top-performing statistical + neural models
- [ ] Fix evaluation merge producing cartesian product (1,280 rows from 80 test rows)

### Pipeline & Code Quality
- [ ] Refactor notebook into modular Python pipeline (`main.py` is stub)
- [ ] Add CLI interface for running forecasts
- [ ] Implement unit tests for data processing and evaluation
- [ ] Add MLflow or experiment tracking for model comparisons
- [ ] Add `.gitignore` entries for `lightning_logs/`, `*.png`, `.ipynb_checkpoints/`

### Evaluation & Submission
- [ ] Use RMSLE (Kaggle competition metric) instead of MAE/RMSE
- [ ] Generate predictions on `test.csv` for Kaggle submission
- [ ] Cross-validate on full dataset (currently 3 folds, 5 series)
- [ ] Benchmark neural models against statistical baselines on same splits

### Deployment
- [ ] Build reproducible training pipeline (config-driven)
- [ ] Add data versioning (DVC or similar)
- [ ] Deploy forecasting service (API or batch)

