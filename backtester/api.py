from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import yaml
import tempfile
import os

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


@app.post("/backtest/upload")
def run_backtest_upload_endpoint(
    file: UploadFile = File(...),
    gaussian_period: int = 20,
    gaussian_multiplier: float = 2.0,
    slope_lookback: int = 4,
    donchian_period: int = 20,
    position_size_percent: float = 1.0,
    initial_capital: float = 10000.0,
    direction: str = "both"
):
    if file.content_type != "text/csv" and not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            content = file.file.read()
            tmp_file.write(content)
            temp_path = tmp_file.name

        try:
            df = load_data(temp_path)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        config = {
            'gaussian_period': gaussian_period,
            'gaussian_multiplier': gaussian_multiplier,
            'slope_lookback': slope_lookback,
            'donchian_period': donchian_period,
            'position_size_percent': position_size_percent,
            'initial_capital': initial_capital,
            'direction': direction
        }

        result = run_backtest(df, config)
        metrics = compute_metrics(result['equity_curve'])
        metrics['trade_count'] = len(result['trades'])
        metrics['equity_curve'] = result['equity_curve']
        metrics['trades'] = result['trades']

        return metrics
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
