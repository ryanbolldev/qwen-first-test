import numpy as np
from backtester.metrics import compute_metrics


def test_metrics_empty():
    metrics = compute_metrics([])
    assert metrics['sharpe'] == 0.0
    assert metrics['max_drawdown'] == 0.0
    assert metrics['win_rate'] == 0.0
    assert metrics['total_return'] == 0.0


def test_metrics_constant_equity():
    metrics = compute_metrics([10000.0] * 100)
    assert metrics['sharpe'] == 0.0
    assert metrics['max_drawdown'] == 0.0
    assert metrics['total_return'] == 0.0


def test_metrics_profitable():
    equity = [10000.0 * (1 + 0.01 * i) for i in range(100)]
    metrics = compute_metrics(equity)
    assert metrics['total_return'] > 0.0
    assert metrics['max_drawdown'] >= 0.0
    assert metrics['sharpe'] >= 0.0
    assert 0.0 <= metrics['win_rate'] <= 1.0
