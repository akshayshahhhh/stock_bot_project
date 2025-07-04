from services.stock_data import fetch_stock_price, fetch_volume_data
from utils.indicators import (
    get_price_data,
    calculate_rsi,
    calculate_ema,
    get_52_week_range_yf as get_52_week_range
)
import pandas as pd

def format_Lakh(number):
    if number is None:
        return "N/A"
    return f"{round(number / 100000, 2)} Lakh"

def detect_hybrid_structure(highs, lows, closes):
    n = len(highs)
    up_highs = sum(y > x for x, y in zip(highs, highs[1:]))
    down_highs = sum(y < x for x, y in zip(highs, highs[1:]))
    up_lows = sum(y > x for x, y in zip(lows, lows[1:]))
    down_lows = sum(y < x for x, y in zip(lows, lows[1:]))

    up_score = (up_highs + up_lows) / (2 * (n - 1))
    down_score = (down_highs + down_lows) / (2 * (n - 1))

    score = max(up_score, down_score)
    if score > 0.75:
        strength = "Strong"
    elif score > 0.60:
        strength = "Normal"
    else:
        strength = "Mixed"

    if up_score > down_score:
        return f"Higher Highs – Higher Lows ({strength} Uptrend)"
    elif down_score > up_score:
        return f"Lower Highs – Lower Lows ({strength} Downtrend)"
    else:
        return "Sideways / Mixed Price Action (Mixed)"

def detect_candlestick_pattern(df):
    last_3 = df.tail(3)
    patterns = []
    for i in range(1, len(last_3)):
        prev = last_3.iloc[i - 1]
        curr = last_3.iloc[i]
        body = abs(curr['Close'] - curr['Open'])
        range_total = curr['High'] - curr['Low']
        if body < 0.25 * range_total:
            patterns.append("Doji")
        if curr['Close'] > curr['Open']:
            if (curr['Open'] - curr['Low']) > 1.5 * body and (curr['High'] - curr['Close']) < body:
                patterns.append("Hammer")
        else:
            if (curr['Close'] - curr['Low']) > 1.5 * body and (curr['High'] - curr['Open']) < body:
                patterns.append("Hammer")
        if curr['Close'] > curr['Open'] and prev['Close'] < prev['Open']:
            if curr['Open'] < prev['Close'] and curr['Close'] > prev['Open']:
                patterns.append("Bullish Engulfing")
        elif curr['Close'] < curr['Open'] and prev['Close'] > prev['Open']:
            if curr['Open'] > prev['Close'] and curr['Close'] < prev['Open']:
                patterns.append("Bearish Engulfing")
    return patterns[-1] if patterns else "No Clear Pattern"

def analyze_stock(symbol):
    symbol = symbol.upper()
    price = fetch_stock_price(symbol)

    if price is None or price <= 0:
        return None, f"Invalid or unavailable price for {symbol}"

    volume = fetch_volume_data(symbol)
    low, high = get_52_week_range(symbol)

    data = get_price_data(symbol, return_full_data=True)
    if data is None or data.empty:
        return None, f"Could not fetch price data for {symbol}."

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    closes = data["Close"]
    volumes = data["Volume"]
    highs = data["High"]
    lows = data["Low"]

    rsi = calculate_rsi(closes)
    emas = calculate_ema(closes)
    ema21 = float(emas['EMA21']) if emas['EMA21'] is not None else None
    ema50 = float(emas['EMA50']) if emas['EMA50'] is not None else None
    ema200 = float(emas['EMA200']) if emas['EMA200'] is not None else None

    if None not in (ema21, ema50, ema200):
        if ema21 > ema50 > ema200:
            trend = "Strong Bullish"
        elif ema21 > ema50 and ema50 > ema200:
            trend = "Bullish"
        elif ema21 < ema50 < ema200:
            trend = "Strong Bearish"
        elif ema21 < ema200:
            trend = "Weak Bearish"
        elif ema21 < ema50 and ema21 > ema200:
            trend = "Pullback or Neutral"
        else:
            trend = "Neutral"
    else:
        trend = "Insufficient Data"

    # Find support
    if ema50 and price and ema50 < price:
        ema_support_base = ema50
        support_label = "(Near EMA 50)"
    else:
        ema_support_base = ema200
        support_label = "(Near EMA 200)"
    if ema50 and ema200 and abs(ema50 - ema200) < 20:
        support_label = "(EMA 50/200 zone)"
    support_zone = f"Rs. {int(ema_support_base - 10)}–Rs. {int(ema_support_base + 10)} {support_label}"

    resistance_min = round(price * 1.02) if price else None
    resistance_max = round(price * 1.04) if price else None
    resistance_zone = f"Rs. {resistance_min}–Rs. {resistance_max} (Estimated Swing High Zone)" if resistance_min else "N/A"

    volume_50dma = volumes.rolling(50).mean().iloc[-1].item()
    volume_signal = "High Volume Breakout Attempt" if volume > 1.2 * volume_50dma else (
        "Low Volume, Possible Consolidation" if volume < 0.8 * volume_50dma else "Average Volume"
    )

    breakout_signal = ""
    if price and volume and resistance_min and volume_50dma:
        volume_threshold = round(1.2 * volume_50dma)
        crossed_resistance = price > resistance_min
        strong_volume = volume > volume_threshold
        if crossed_resistance and strong_volume:
            breakout_signal = f"🚨 Potential Breakout: Price Above Swing Resistance of Rs. {resistance_min} with Volume Surge of ~{format_Lakh(volume)} Shares"
        elif crossed_resistance:
            breakout_signal = f"🚨 Potential Breakout: Price has Crossed Resistance of Rs. {resistance_min} but Strong Volume of ~{format_Lakh(volume_threshold)} Shares is Missing"
        elif strong_volume:
            breakout_signal = f"🚨 Potential Breakout: Strong Volume Present (~{format_Lakh(volume)}) but Price has not yet Crossed Rs. {resistance_min}"
        else:
            breakout_signal = f"🚨 Potential Breakout: Only if Price Crosses Rs. {resistance_min} with Strong Volume of ~{format_Lakh(volume_threshold)} Shares"

    daily_structure = detect_hybrid_structure(highs[-10:], lows[-10:], closes[-10:])
    weekly_data = data.resample('W').agg({'High': 'max', 'Low': 'min', 'Close': 'last'}).dropna()
    weekly_structure = detect_hybrid_structure(
        weekly_data["High"][-15:], weekly_data["Low"][-15:], weekly_data["Close"][-15:]
    )
    candle_pattern = detect_candlestick_pattern(data)

    result = {
        "symbol": symbol,
        "price": price,
        "low": low,
        "high": high,
        "rsi": rsi,
        "ema_21": ema21,
        "ema_50": ema50,
        "ema_200": ema200,
        "trend": trend,
        "support_zone": support_zone,
        "resistance_zone": resistance_zone,
        "volume": volume,
        "volume_avg": volume_50dma,
        "volume_signal": volume_signal,
        "breakout_signal": breakout_signal,
        "candlestick": candle_pattern,
        "structure_daily": daily_structure,
        "structure_weekly": weekly_structure
    }

    return result, None

# Export for unified import
generate_stock_report = analyze_stock
