import pandas as pd


def set_unique_id(df) -> pd.DataFrame:
    df['unique_id'] = 'store_' + df['store_nbr'].astype('str') + '_' + df['family']
    return df

def clean_na(df):
    pass
    
def preprocess_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    df = df[["unique_id", "date", "sales"]].rename(columns={"date": "ds", "sales": "y"})

    max_date_per_series = df.groupby("unique_id", as_index=False)["ds"].transform("max")
    cutoff = max_date_per_series - pd.Timedelta(days=16)

    train_df = df[df["ds"] <= cutoff]
    val_df = df[df["ds"] <= cutoff]

    return train_df, val_df
