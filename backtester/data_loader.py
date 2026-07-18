import pandas as pd
from pathlib import Path


def load_data(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise ValueError(f"Data file not found: {path}")
    df = pd.read_csv(p)
    required_cols = {'date', 'open', 'high', 'low', 'close', 'volume'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    try:
        df['date'] = pd.to_datetime(df['date'], utc=True)
    except Exception:
        raise ValueError("Failed to parse 'date' column as datetime")
    df = df.set_index('date').sort_index()
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        if df[col].isna().any():
            raise ValueError(f"NaN values in column: {col}")
        if (df[col] <= 0).any():
            raise ValueError(f"Non-positive values in column: {col}")
    if df.empty:
        raise ValueError("Dataframe is empty after loading")
    return df
