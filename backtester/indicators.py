import numpy as np
import pandas as pd


def gaussian_weights(period: int) -> np.ndarray:
    x = np.arange(period)
    mu = (period - 1) / 2.0
    sigma = period / 6.0
    w = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    return w / w.sum()


def gaussian_ma(close: pd.Series, period: int) -> pd.Series:
    weights = gaussian_weights(period)
    return close.rolling(window=period, min_periods=period).apply(
        lambda x: np.dot(x, weights), raw=True
    )


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int) -> pd.Series:
    tr = pd.DataFrame({
        'h_l': high - low,
        'h_c': (high - close.shift()).abs(),
        'l_c': (low - close.shift()).abs()
    }).max(axis=1)
    return tr.rolling(window=period, min_periods=period).mean()


def donchian_bands(close: pd.Series, period: int) -> tuple[pd.Series, pd.Series]:
    upper = close.rolling(window=period, min_periods=period).max()
    lower = close.rolling(window=period, min_periods=period).min()
    return upper, lower


def detect_trend(centerline: pd.Series, lookback: int) -> pd.Series:
    diff = centerline - centerline.shift(lookback)
    return pd.Series(
        np.where(diff > 0, 1, np.where(diff < 0, -1, 0)),
        index=centerline.index,
        dtype=int
    )
