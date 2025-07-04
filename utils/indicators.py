import yfinance as yf
import pandas as pd

def get_price_data(symbol, return_full_data=False):
    """
    Fetches OHLCV data for a given symbol using yfinance.
    Returns either full DataFrame or just the 'Close' Series.
    """
    data = yf.download(symbol + ".NS", period="1y", interval="1d", progress=False)
    if data.empty:
        return None if return_full_data else pd.Series(dtype=float)
    if return_full_data:
        return data
    else:
        return data["Close"]

def calculate_rsi(series, period=14):
    """
    Calculate RSI for a pandas Series.
    Returns last RSI value as float.
    """
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=period, min_periods=1).mean()
    ma_down = down.rolling(window=period, min_periods=1).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])

def calculate_ema(series):
    """
    Calculate EMA 21, 50, 200 for a pandas Series.
    Returns a dict of latest EMA values.
    """
    ema_21 = series.ewm(span=21, adjust=False).mean().iloc[-1]
    ema_50 = series.ewm(span=50, adjust=False).mean().iloc[-1]
    ema_200 = series.ewm(span=200, adjust=False).mean().iloc[-1]
    return {
        'EMA21': float(ema_21),
        'EMA50': float(ema_50),
        'EMA200': float(ema_200)
    }

def get_52_week_range_yf(symbol):
    """
    Fetches 1-year data and returns (low, high) for 52-week range.
    """
    data = yf.download(symbol + ".NS", period="1y", interval="1d", progress=False)
    if not data.empty:
        low = int(data["Low"].min())
        high = int(data["High"].max())
        return low, high
    else:
        return None, None
