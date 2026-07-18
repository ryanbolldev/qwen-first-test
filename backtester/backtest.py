import pandas as pd
import numpy as np
from .strategy import generate_signals


def run_backtest(df: pd.DataFrame, config: dict) -> dict:
    position_size = config['position_size_percent'] / 100.0
    initial_capital = config['initial_capital']
    direction = config['direction']

    df = generate_signals(df, config)

    capital = initial_capital
    position = 0
    equity_curve = []
    trades = []

    for i in range(len(df)):
        row = df.iloc[i]
        price = row['close']

        # Exit logic
        if position > 0 and row['exit_long']:
            equity = capital + position * (price - df.iloc[i-1]['close'])
            capital = equity
            position = 0
            trades.append({
                'index': i,
                'type': 'long_exit',
                'price': price,
                'equity': capital
            })
        elif position < 0 and row['exit_short']:
            equity = capital + position * (df.iloc[i-1]['close'] - price)
            capital = equity
            position = 0
            trades.append({
                'index': i,
                'type': 'short_exit',
                'price': price,
                'equity': capital
            })

        # Entry logic
        if position == 0:
            if row['long_signal']:
                units = int((capital * position_size) / price)
                if units > 0:
                    position = units
                    trades.append({
                        'index': i,
                        'type': 'long_entry',
                        'price': price,
                        'equity': capital
                    })
            elif row['short_signal']:
                units = int((capital * position_size) / price)
                if units > 0:
                    position = -units
                    trades.append({
                        'index': i,
                        'type': 'short_entry',
                        'price': price,
                        'equity': capital
                    })

        # Equity calculation
        if position > 0:
            equity = capital + position * (price - df.iloc[i-1]['close']) if i > 0 else capital
        elif position < 0:
            equity = capital + position * (df.iloc[i-1]['close'] - price) if i > 0 else capital
        else:
            equity = capital

        equity_curve.append(equity)

    return {
        'equity_curve': equity_curve,
        'trades': trades
    }
