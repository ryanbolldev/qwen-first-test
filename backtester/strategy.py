import pandas as pd
from .indicators import gaussian_ma, atr, donchian_bands, detect_trend


def generate_signals(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    gaussian_period = config['gaussian_period']
    gaussian_mult = config['gaussian_multiplier']
    slope_lookback = config['slope_lookback']
    donchian_period = config['donchian_period']
    direction = config['direction']

    # Resample to 4H for trend filter
    df4 = df.resample('4H').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

    # 4H Gaussian trend
    gma4 = gaussian_ma(df4['close'], gaussian_period)
    atr4 = atr(df4['high'], df4['low'], df4['close'], gaussian_period)
    upper_band4 = gma4 + gaussian_mult * atr4
    lower_band4 = gma4 - gaussian_mult * atr4
    trend4 = detect_trend(gma4, slope_lookback)

    # Align 4H trend to 1H index (forward fill)
    trend4 = trend4.reindex(df.index, method='ffill')
    trend4 = trend4.fillna(0)

    # 1H Donchian
    upper1, lower1 = donchian_bands(df['close'], donchian_period)

    # Signals
    long_signal = (df['close'] > upper1) & (trend4 == 1)
    short_signal = (df['close'] < lower1) & (trend4 == -1)

    if direction == 'long_only':
        short_signal = False
    elif direction == 'short_only':
        long_signal = False

    exit_long = df['close'] < lower1
    exit_short = df['close'] > upper1

    df = df.copy()
    df['long_signal'] = long_signal.astype(int)
    df['short_signal'] = short_signal.astype(int)
    df['exit_long'] = exit_long.astype(int)
    df['exit_short'] = exit_short.astype(int)
    df['trend'] = trend4

    return df
