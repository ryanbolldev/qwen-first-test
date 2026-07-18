import pandas as pd
import numpy as np
from backtester.indicators import gaussian_ma, atr, donchian_bands, detect_trend


def test_gaussian_ma_length():
    close = pd.Series(np.random.randn(100))
    gma = gaussian_ma(close, 20)
    assert len(gma.dropna()) == len(close) - 19


def test_gaussian_ma_weights_sum():
    from backtester.indicators import gaussian_weights
    w = gaussian_weights(20)
    assert np.isclose(w.sum(), 1.0)


def test_atr_length():
    high = pd.Series(np.random.randn(100).cumsum() + 100)
    low = high - pd.Series(np.random.rand(100))
    close = high - pd.Series(np.random.rand(100))
    atr_series = atr(high, low, close, 14)
    assert len(atr_series.dropna()) == len(close) - 13


def test_donchian_bands_length():
    close = pd.Series(np.random.randn(100).cumsum() + 100)
    upper, lower = donchian_bands(close, 20)
    assert len(upper.dropna()) == len(close) - 19
    assert len(lower.dropna()) == len(close) - 19
    assert (upper >= lower).all()


def test_detect_trend_direction():
    centerline = pd.Series([100, 101, 102, 101, 100, 99, 98])
    trend = detect_trend(centerline, 2)
    assert trend.iloc[2] == 1
    assert trend.iloc[4] == -1
    assert trend.iloc[6] == -1
