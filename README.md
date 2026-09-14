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

- [x] Set up MLflow tracking server (local or remote)
  - **Done:** `mlflow ui` serves tracking UI; runs persist across restarts
- [x] Define experiment naming convention (e.g., `{model_type}/{feature_set}/{date}`)
  - **Done:** Convention documented; all new runs follow it consistently
- [x] Log model type and architecture config per run
  - **Done:** Every logged run includes model type and full architecture params
- [x] Log feature set used per run (which exogenous variables included)
  - **Done:** Every logged run tags which exogenous variables were active
- [x] Log CV fold metrics individually (MAE, RMSE, RMSLE per fold)
  - **Done:** Per-fold metrics visible in MLflow for any run with CV
- [x] Log aggregated CV metrics (mean ± std across folds)
  - **Done:** Mean and std metrics logged as top-level run metrics
- [x] Log hyperparameters per run (learning rate, layers, epochs, etc.)
  - **Done:** All tunable params logged; reproducible from logged values alone
- [x] Log training duration and resource usage per run
  - **Done:** Wall time and GPU/CPU usage logged per run
- [x] Build query to retrieve best model per `unique_id` ranked by RMSLE
  - **Done:** Query returns correct best model for any given series
- [x] Build query to compare models across feature sets for same series
  - **Done:** Query returns comparison table filterable by series and feature set
- [x] Register best-performing model per series in MLflow Model Registry
  - **Done:** Registry contains one model per series; `mlflow.pyfunc.load_model` loads it
- [x] Tag registered models with stage (staging/production)
  - **Done:** All registered models tagged; stage transitions logged

### 2. Critical Fixes & Repo Hygiene

- [x] Fix evaluation merge producing cartesian product (1,280 rows from 80 test rows)
- [x] Add `.gitignore` entries for `lightning_logs/`, `*.png`, `.ipynb_checkpoints/`
- [x] Use RMSLE (Kaggle competition metric) instead of MAE/RMSE

### 3. Data & Feature Engineering

- [ ] Handle 31.3% zero-sales entries (intermittent demand strategy)
  - **Done:** Zero-sales strategy chosen, implemented, and RMSLE improved or justified vs baseline
  - [ ] Analyze zero-sales distribution by store, family, and day of week
    - **Done:** Distribution summary table/plot exists showing zero-sales % by store, family, weekday
  - [ ] Decide strategy: separate zero/non-zero model, Croston's method, or keep as-is
    - **Done:** Decision documented with rationale referencing analysis results
  - [ ] Implement chosen zero-sales handling
    - **Done:** Pipeline applies chosen strategy; no raw zeros leak into model when strategy filters them
  - [ ] Validate impact on RMSLE vs baseline
    - **Done:** Before/after RMSLE comparison logged in MLflow
- [ ] Improve oil price missing value imputation (currently ffill/bfill)
  - **Done:** Chosen method implemented; forecast accuracy same or better than ffill/bfill
  - [ ] Evaluate interpolation methods (linear, spline) vs ffill/bfill
    - **Done:** Comparison of imputation methods with RMSLE impact documented
  - [ ] Implement chosen imputation and compare forecast accuracy
    - **Done:** Pipeline uses new imputation; MLflow run shows accuracy delta
- [ ] Incorporate holidays.csv as exogenous variable
  - **Done:** Holiday features in training DataFrame; model accepts them without error
  - [ ] Parse holiday types (national, regional, local, transfer, bridge)
    - **Done:** All 5 holiday types parsed; no unparsed rows remain
  - [ ] Map regional/local holidays to relevant stores
    - **Done:** Regional/local holidays mapped to correct store subset; national applied to all
  - [ ] Create binary/categorical holiday features
    - **Done:** Holiday columns present in feature DataFrame with correct dtype
- [ ] Incorporate transactions.csv as exogenous variable
  - **Done:** Transaction features available for training; test-set strategy implemented
  - [ ] Join transaction counts to training data by store and date
    - **Done:** Transaction column present in merged training DataFrame; no NaN in training rows
  - [ ] Handle missing transaction dates (test set has no transactions)
    - **Done:** Missing dates filled or excluded; no NaN crashes at inference
  - [ ] Decide strategy for test-set transaction forecasting or exclusion
    - **Done:** Decision documented; pipeline handles test set without transaction data
- [ ] Add promotion (`onpromotion`) as exogenous regressor
  - **Done:** `onpromotion` column in feature matrix; model trains and predicts with it
- [ ] Engineer store metadata features from stores.csv
  - **Done:** Store metadata columns in feature DataFrame; no missing values
  - [ ] Add city and state as categorical features
    - **Done:** City/state columns encoded and present in feature matrix
  - [ ] Add store type as categorical feature
    - **Done:** Store type column encoded and present
  - [ ] Add cluster as categorical/ordinal feature
    - **Done:** Cluster column present with chosen encoding (categorical or ordinal)
- [ ] Scale to all 1,782 time series (currently using 5 subset categories)
  - **Done:** Full pipeline runs on 1,782 series; results validated against subset baseline
  - [ ] Profile memory and runtime on current 5-series subset
    - **Done:** Memory peak and wall time recorded for 5-series run
  - [ ] Test on intermediate subset (e.g., 50 series) for scaling bottlenecks
    - **Done:** 50-series run completes; bottlenecks identified and addressed
  - [ ] Run full 1,782-series pipeline and validate results
    - **Done:** 1,782-series run completes; RMSLE within expected range

### 4. Modeling — Nixtla (Statistical + Neural)

- [ ] Add exogenous variables to NeuralForecast models
  - **Done:** Models train with exogenous inputs; RMSLE comparison vs univariate logged
  - [ ] Add oil price as exogenous input
    - **Done:** Oil price column accepted by model; no shape/NaN errors
  - [ ] Add promotion flag as exogenous input
    - **Done:** Promotion flag accepted by model; no shape/NaN errors
  - [ ] Validate exogenous features improve RMSLE vs univariate baseline
    - **Done:** MLflow comparison shows exogenous vs univariate RMSLE delta
- [ ] Tune NeuralForecast models
  - **Done:** Best hyperparams per model logged; top performers selected
  - [ ] Tune LSTM: grid search `max_steps`, hidden size, learning rate
    - **Done:** Grid search complete; best LSTM config logged in MLflow
  - [ ] Tune GRU: grid search `max_steps`, hidden size, learning rate
    - **Done:** Grid search complete; best GRU config logged in MLflow
  - [ ] Tune RNN: grid search `max_steps`, hidden size, learning rate
    - **Done:** Grid search complete; best RNN config logged in MLflow
  - [ ] Compare tuned models and select top performers
    - **Done:** Comparison table produced; top N models identified
- [x] Try NHITS and PatchTST from NeuralForecast
- [ ] Implement hierarchical forecasting
  - **Done:** Reconciled forecasts produced; coherent across hierarchy levels
  - [ ] Define hierarchy levels (store → family → total)
    - **Done:** Hierarchy matrix defined; aggregation produces correct totals
  - [ ] Generate base forecasts at each level
    - **Done:** Base forecasts exist at every hierarchy level
  - [ ] Apply reconciliation method (bottom-up, top-down, or MinTrace)
    - **Done:** Reconciliation applied; bottom-level forecasts sum to top-level
- [ ] Ensemble top-performing statistical + neural models
  - **Done:** Ensemble RMSLE beats best single model (or justified why not)
  - [ ] Select top N models per series by CV RMSLE
    - **Done:** Top N models identified per series from CV results
  - [ ] Test ensemble strategies (simple average, weighted average, stacking)
    - **Done:** At least 3 strategies tested; results logged
  - [ ] Validate ensemble RMSLE vs best single model
    - **Done:** Comparison logged in MLflow; winner selected

---

### MILESTONE: Notebook → Modular Python Project

**Gate:** Complete sections 1–4 in the notebook before proceeding. Everything below this line must be built as Python modules, not notebook cells.

**Why:** The notebook served its purpose — data exploration, baseline models, experiment tracking patterns. Gradient boosting ensembles, full-scale CV, and deployment require testable, config-driven code that doesn't belong in a notebook.

**Before crossing this gate:**

- [ ] All section 1–4 `[x]` items verified and runs reproducible
- [ ] Best notebook model identified (winner from statistical vs neural comparison)
- [ ] `evaluate_models()` and data loading patterns validated — ready to extract
- [ ] MLflow experiment structure finalized (no more schema changes)

**Transition steps:**

1. Extract data loading/cleaning → `src/data.py`
2. Extract feature engineering → `src/features.py`
3. Extract model training/evaluation → `src/models.py`
4. Wire together in `main.py` with CLI args and YAML config
5. Add unit tests for each module
6. All new modeling (sections 5+) goes into modules, not notebook

**After crossing:** The notebook becomes a visualization/demo tool only. All training, evaluation, and submission runs go through `python main.py`.

---

### 5. Modeling — Gradient Boosting Ensemble (Kaggle Winning Approach)

#### Architecture

Hybrid of two forecasting strategies:

1. **Recursive Global Ensemble** — weighted blend of LightGBM (35%), CatBoost (40%), XGBoost (25%). Uses log-transformed target and weighted training emphasizing recent observations.
2. **Direct Multi-Horizon Forecasting** — 16 separate direct models (one per forecast horizon day).
3. **Final prediction** — 60% recursive ensemble + 40% direct multi-horizon ensemble.

#### Feature Engineering

- [ ] Time features
  - **Done:** All time columns present in feature DataFrame with correct values
  - [ ] Day of week, day of year, week of year, month, year
    - **Done:** Columns present; spot-check matches calendar for sample dates
  - [ ] Month-end / month-start binary flags
    - **Done:** Flags correct for known month boundaries
  - [ ] Fourier seasonal terms (annual and weekly cycles)
    - **Done:** Sine/cosine pairs present; period matches 365.25 (annual) and 7 (weekly)
- [ ] Lag features
  - **Done:** Lag and rolling columns present; no data leakage from future values
  - [ ] Sales lags: 1, 7, 14, 28 days
    - **Done:** Lag columns present; values match manual shift check
  - [ ] Rolling mean: 7-day and 28-day windows
    - **Done:** Rolling mean columns present; NaN only in expected warm-up rows
  - [ ] Rolling std: 7-day and 28-day windows
    - **Done:** Rolling std columns present; NaN only in expected warm-up rows
- [ ] Promotion features
  - **Done:** Promotion lag and rolling columns present in feature matrix
  - [ ] Promotion lags (1, 7, 14 days)
    - **Done:** Lag columns present; values match manual shift check
  - [ ] Promotion rolling averages (7-day, 28-day windows)
    - **Done:** Rolling average columns present; values within [0, 1] range
- [ ] Target encoding
  - **Done:** Target-encoded columns present; computed on training fold only (no leakage)
  - [ ] Store average sales
    - **Done:** Column present; values match groupby mean on training data
  - [ ] Family average sales
    - **Done:** Column present; values match groupby mean on training data
  - [ ] Store-family interaction average sales
    - **Done:** Column present; values match groupby mean on training data
- [ ] External data integration
  - **Done:** All external feature columns present; no unexpected NaN
  - [ ] Oil price features (current, lagged, rolling average)
    - **Done:** Oil columns present; lagged values match manual shift
  - [ ] Store metadata (type, cluster, city, state)
    - **Done:** Metadata columns merged; no missing values for known stores
  - [ ] Transaction counts (lagged, rolling)
    - **Done:** Transaction columns present; test-set handling applied
  - [ ] Holiday/event binary signals
    - **Done:** Holiday columns present; known holidays flagged correctly

#### Models

- [ ] LightGBM with GPU-accelerated training
  - **Done:** Tuned LightGBM trains on GPU; best params logged in MLflow
  - [ ] Baseline LightGBM model with default params
    - **Done:** Baseline RMSLE logged; serves as tuning reference
  - [ ] Hyperparameter tuning (num_leaves, learning_rate, max_depth, reg)
    - **Done:** Best params found; RMSLE improvement over baseline logged
- [ ] CatBoost with GPU-accelerated training
  - **Done:** Tuned CatBoost trains on GPU; best params logged in MLflow
  - [ ] Baseline CatBoost model with default params
    - **Done:** Baseline RMSLE logged; serves as tuning reference
  - [ ] Hyperparameter tuning (depth, learning_rate, iterations, l2_reg)
    - **Done:** Best params found; RMSLE improvement over baseline logged
- [ ] XGBoost with GPU-accelerated training
  - **Done:** Tuned XGBoost trains on GPU; best params logged in MLflow
  - [ ] Baseline XGBoost model with default params
    - **Done:** Baseline RMSLE logged; serves as tuning reference
  - [ ] Hyperparameter tuning (max_depth, learning_rate, n_estimators, reg)
    - **Done:** Best params found; RMSLE improvement over baseline logged
- [ ] Log target transformation + recent-observation weighted learning
  - **Done:** log1p/expm1 roundtrip correct; sample weights decay verified
  - [ ] Implement log1p target transform with expm1 inverse
    - **Done:** Transform applied; `expm1(log1p(y)) == y` holds for all training targets
  - [ ] Implement sample weights decaying by recency
    - **Done:** Recent rows weighted higher; weight distribution plotted/verified
- [ ] Weighted recursive ensemble (LGB 35% / CB 40% / XGB 25%)
  - **Done:** Ensemble predictions produced; weights validated or optimized via CV
  - [ ] Train each model with shared feature pipeline
    - **Done:** All 3 models train on identical feature matrix
  - [ ] Validate weight allocation via CV (or optimize weights)
    - **Done:** Weight search results logged; final weights chosen
- [ ] Direct multi-horizon models (16 independent horizon models)
  - **Done:** 16 models trained; per-horizon RMSLE logged
  - [ ] Build training data per horizon (day 1 through day 16)
    - **Done:** 16 separate training sets created; target correctly offset per horizon
  - [ ] Train one model per horizon day
    - **Done:** 16 models trained; each logged separately in MLflow
  - [ ] Validate per-horizon predictions independently
    - **Done:** Per-horizon RMSLE computed; no horizon significantly worse than others
- [ ] Final hybrid blend (60% recursive / 40% direct)
  - **Done:** Hybrid RMSLE beats both recursive-only and direct-only
  - [ ] Combine recursive and direct predictions
    - **Done:** Blended predictions match expected shape; no NaN
  - [ ] Validate hybrid RMSLE vs individual strategies
    - **Done:** Comparison table: recursive vs direct vs hybrid RMSLE logged

### 6. Evaluation & Submission

- [ ] Cross-validate on full dataset
  - **Done:** CV runs on all 1,782 series; per-fold and aggregate RMSLE recorded
  - [ ] Expand from 5 series to full 1,782 series
    - **Done:** CV pipeline processes 1,782 series without OOM or timeout
  - [ ] Increase fold count if compute allows (currently 3 folds)
    - **Done:** Fold count set to max feasible; documented why if kept at 3
  - [ ] Record per-series and aggregate RMSLE per fold
    - **Done:** Per-series and aggregate metrics logged in MLflow per fold
- [ ] Benchmark neural models against statistical baselines on same splits
  - **Done:** Comparison table with per-family and aggregate RMSLE exists
  - [ ] Run statistical baselines (SeasonalNaive, AutoETS, AutoARIMA) on same CV splits
    - **Done:** All 3 baselines produce predictions on same folds; metrics logged
  - [ ] Run neural models on same CV splits
    - **Done:** Neural models produce predictions on same folds; metrics logged
  - [ ] Compare per-family and aggregate RMSLE
    - **Done:** Comparison table shows winner per family and overall
- [ ] Benchmark gradient boosting ensemble against all other approaches
  - **Done:** GB ensemble results added to comparison table; overall winner identified
  - [ ] Run gradient boosting ensemble on same CV splits
    - **Done:** GB ensemble predictions on same folds; metrics logged
  - [ ] Produce comparison table: statistical vs neural vs gradient boosting
    - **Done:** Table saved to `reports/model_comparison.md`; all approaches compared
- [ ] Generate Kaggle submission
  - **Done:** Submission CSV uploaded; public leaderboard score recorded
  - [ ] Produce predictions on `test.csv` with best model/ensemble
    - **Done:** Predictions cover all test rows; no NaN values
  - [ ] Format submission CSV per Kaggle spec
    - **Done:** CSV has correct columns (`id`, `sales`); row count matches test set
  - [ ] Submit and record public leaderboard score
    - **Done:** Score recorded in MLflow and README; position noted

### 7. Pipeline & Code Quality

- [ ] Refactor notebook into modular Python pipeline (`main.py` is stub)
  - **Done:** `python main.py` runs end-to-end; notebook logic lives in modules
  - [ ] Extract data loading and preprocessing into `data.py`
    - **Done:** `data.py` loads and cleans data; notebook imports from it
  - [ ] Extract feature engineering into `features.py`
    - **Done:** `features.py` builds feature matrix; notebook imports from it
  - [ ] Extract model training and evaluation into `models.py`
    - **Done:** `models.py` trains and evaluates; notebook imports from it
  - [ ] Wire modules together in `main.py`
    - **Done:** `main.py` calls data → features → models → output; runs without error
- [ ] Add CLI interface for running forecasts
  - **Done:** `python main.py train`, `evaluate`, `predict` work from command line
  - [ ] Add argument parsing (model type, data path, output path, config)
    - **Done:** `--help` shows all args; invalid args produce clear error
  - [ ] Support train, evaluate, and predict subcommands
    - **Done:** All 3 subcommands run; each produces expected output
- [ ] Implement unit tests for data processing and evaluation
  - **Done:** `pytest` passes; covers data, features, and evaluation
  - [ ] Tests for data loading and cleaning functions
    - **Done:** Tests verify loading, NaN handling, dtype correctness
  - [ ] Tests for feature engineering functions
    - **Done:** Tests verify feature columns, no leakage, correct values
  - [ ] Tests for evaluation metric calculations (RMSLE)
    - **Done:** RMSLE tests match known hand-calculated values

### 8. Deployment

- [ ] Build reproducible training pipeline (config-driven)
  - **Done:** Fresh clone + config file → full training run with no code edits
  - [ ] Create YAML/TOML config for model params, data paths, feature toggles
    - **Done:** Config file exists; all tunable params and paths defined in it
  - [ ] Ensure pipeline runs end-to-end from config without code changes
    - **Done:** `python main.py train --config config.yaml` succeeds on clean checkout
- [ ] Add data versioning (DVC or similar)
  - **Done:** Raw data and artifacts tracked; `dvc pull` restores them
  - [ ] Initialize DVC in repo
    - **Done:** `.dvc/` directory exists; `dvc status` runs clean
  - [ ] Track raw datasets and processed artifacts
    - **Done:** `.dvc` files committed for all datasets; `dvc pull` restores data
- [ ] Deploy forecasting service (API or batch)
  - **Done:** Service runs; health check returns 200; predictions return valid JSON/CSV
  - [ ] Choose deployment mode (REST API vs scheduled batch job)
    - **Done:** Decision documented with rationale
  - [ ] Implement chosen deployment
    - **Done:** Service starts and serves predictions
  - [ ] Add health check and basic monitoring
    - **Done:** `/health` endpoint (or equivalent) returns status; basic metrics collected
