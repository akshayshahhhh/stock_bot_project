import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def fetch_stock_price(symbol):
    try:
        # Try fetching live intraday price (1-minute interval)
        data = yf.download(symbol + ".NS", period="1d", interval="1m", progress=False, auto_adjust=False)
        if data is not None and not data.empty:
            return float(data["Close"].iloc[-1])

        # Fallback to previous day's close if intraday data fails
        data = yf.download(symbol + ".NS", period="2d", interval="1d", progress=False, auto_adjust=False)
        if data is not None and not data.empty:
            return float(data["Close"].iloc[-1])

        logger.warning(f"Price fetch failed for {symbol}")
        return None
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None

def fetch_volume_data(symbol):
    try:
        data = yf.download(symbol + ".NS", period="2d", interval="1d", progress=False, auto_adjust=False)
        if data is not None and not data.empty:
            return int(data["Volume"].iloc[-1])
        return None
    except Exception as e:
        logger.error(f"Error fetching volume for {symbol}: {e}")
        return None