import numpy as np
import pandas as pd


def compute_metrics(equity_curve: list) -> dict:
    if not equity_curve:
        return {
            'sharpe': 0.0,
            'max_drawdown': 0.0,
            'win_rate': 0.0,
            'total_return': 0.0
        }

    equity = np.array(equity_curve)
    returns = np.diff(equity) / equity[:-1]
    returns = np.nan_to_num(returns, nan=0.0)

    total_return = (equity[-1] - equity[0]) / equity[0] if equity[0] != 0 else 0.0

    drawdowns = []
    peak = equity[0]
    for e in equity:
        if e > peak:
            peak = e
        drawdowns.append((peak - e) / peak if peak != 0 else 0.0)
    max_drawdown = max(drawdowns) if drawdowns else 0.0

    if len(returns) > 0 and returns.std(ddof=1) != 0:
        sharpe = (returns.mean() / returns.std(ddof=1)) * np.sqrt(252 * 24)  # hourly
    else:
        sharpe = 0.0

    wins = np.sum(returns > 0)
    total_trades = len(returns)
    win_rate = wins / total_trades if total_trades > 0 else 0.0

    return {
        'sharpe': float(sharpe),
        'max_drawdown': float(max_drawdown),
        'win_rate': float(win_rate),
        'total_return': float(total_return)
    }
