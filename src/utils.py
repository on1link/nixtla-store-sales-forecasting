import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_log_error

# Callable function to compute RMSLE using utilsforecast evaluate function
def rmsle(df, models, id_col="unique_id", target_col="y") -> pd.DataFrame:
    out = {id_col: [], "metric": []}
    for uid, g in df.groupby(id_col):
        out[id_col].append(uid)
        out["metric"].append("rmsle")
        for model in models:
            out.setdefault(model, []).append(
                root_mean_squared_log_error(g[target_col], g[model])
            )


    return pd.DataFrame(out)

def evaluate_models(df: pd.DataFrame, model_cols: list) -> pd.DataFrame:
    results = []
    for uid in df['unique_id'].unique():
        mask = df['unique_id'] == uid
        for model in model_cols:
            y_true = df.loc[mask, 'y'].values
            y_pred = df.loc[mask, model].values
            y_pred_clipped = np.clip(y_pred, 0, None)
            val_mae = mean_absolute_error(y_true, y_pred)
            val_rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            val_rmsle = root_mean_squared_log_error(y_true, y_pred_clipped)
            results.append({'unique_id': uid, 'model': model, 'MAE': val_mae, 'RMSE': val_rmse, 'RMSLE': val_rmsle})

    return pd.DataFrame(results)