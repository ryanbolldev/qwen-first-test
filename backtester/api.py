from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import yaml

from .data_loader import load_data
from .backtest import run_backtest
from .metrics import compute_metrics

app = FastAPI(title="Crypto Backtester API")


class BacktestRequest(BaseModel):
    data_path: str = "data/btc_1h.csv"
    gaussian_period: int = 20
    gaussian_multiplier: float = 2.0
    slope_lookback: int = 4
    donchian_period: int = 20
    position_size_percent: float = 1.0
    initial_capital: float = 10000.0
    direction: str = "both"


@app.post("/backtest")
def run_backtest_endpoint(req: BacktestRequest):
    try:
        df = load_data(req.data_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    config = {
        'gaussian_period': req.gaussian_period,
        'gaussian_multiplier': req.gaussian_multiplier,
        'slope_lookback': req.slope_lookback,
        'donchian_period': req.donchian_period,
        'position_size_percent': req.position_size_percent,
        'initial_capital': req.initial_capital,
        'direction': req.direction
    }

    result = run_backtest(df, config)
    metrics = compute_metrics(result['equity_curve'])
    metrics['trade_count'] = len(result['trades'])
    metrics['equity_curve'] = result['equity_curve']
    metrics['trades'] = result['trades']

    return metrics
