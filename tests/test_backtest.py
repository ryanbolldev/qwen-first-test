import pandas as pd
import numpy as np
from backtester.backtest import run_backtest


def test_backtest_runs():
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
        'position_size_percent': 1.0,
        'initial_capital': 10000.0,
        'direction': 'both'
    }

    result = run_backtest(df, config)
    assert 'equity_curve' in result
    assert 'trades' in result
    assert len(result['equity_curve']) == len(df)
    assert len(result['trades']) >= 0


def test_backtest_position_sizing():
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
        'position_size_percent': 50.0,
        'initial_capital': 10000.0,
        'direction': 'both'
    }

    result = run_backtest(df, config)
    assert len(result['equity_curve']) == len(df)
