import pandas as pd
import numpy as np
from backtester.strategy import generate_signals


def test_strategy_signal_generation():
    dates = pd.date_range('2023-01-01', periods=100, freq='1H')
    close = pd.Series(np.random.randn(100).cumsum() + 100, index=dates)
    high = close + pd.Series(np.random.rand(100))
    low = close - pd.Series(np.random.rand(100))
    volume = pd.Series(np.random.rand(100) * 1000, index=dates)

    df = pd.DataFrame({
        'open': close,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })

    config = {
        'gaussian_period': 10,
        'gaussian_multiplier': 1.0,
        'slope_lookback': 2,
        'donchian_period': 5,
        'direction': 'both'
    }

    result = generate_signals(df, config)
    assert 'long_signal' in result.columns
    assert 'short_signal' in result.columns
    assert 'exit_long' in result.columns
    assert 'exit_short' in result.columns
    assert 'trend' in result.columns
    assert result['trend'].isin([-1, 0, 1]).all()


def test_strategy_long_only():
    dates = pd.date_range('2023-01-01', periods=100, freq='1H')
    close = pd.Series(np.random.randn(100).cumsum() + 100, index=dates)
    high = close + pd.Series(np.random.rand(100))
    low = close - pd.Series(np.random.rand(100))
    volume = pd.Series(np.random.rand(100) * 1000, index=dates)

    df = pd.DataFrame({
        'open': close,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })

    config = {
        'gaussian_period': 10,
        'gaussian_multiplier': 1.0,
        'slope_lookback': 2,
        'donchian_period': 5,
        'direction': 'long_only'
    }

    result = generate_signals(df, config)
    assert (result['short_signal'] == 0).all()
    assert (result['long_signal'] >= 0).all()


def test_strategy_short_only():
    dates = pd.date_range('2023-01-01', periods=100, freq='1H')
    close = pd.Series(np.random.randn(100).cumsum() + 100, index=dates)
    high = close + pd.Series(np.random.rand(100))
    low = close - pd.Series(np.random.rand(100))
    volume = pd.Series(np.random.rand(100) * 1000, index=dates)

    df = pd.DataFrame({
        'open': close,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })

    config = {
        'gaussian_period': 10,
        'gaussian_multiplier': 1.0,
        'slope_lookback': 2,
        'donchian_period': 5,
        'direction': 'short_only'
    }

    result = generate_signals(df, config)
    assert (result['long_signal'] == 0).all()
    assert (result['short_signal'] >= 0).all()
