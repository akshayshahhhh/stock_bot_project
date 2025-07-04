import requests

# Headers and session setup
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive"
}

session = requests.Session()
session.headers.update(HEADERS)

# Base URL builder
def get_nse_equity_url(symbol):
    return f"https://www.nseindia.com/api/quote-equity?symbol={symbol.upper()}"

# Get CMP
def get_cmp(symbol):
    try:
        session.get("https://www.nseindia.com", timeout=5)  # Warm-up
        url = get_nse_equity_url(symbol)
        response = session.get(url, timeout=5)
        data = response.json()
        return float(data['priceInfo']['lastPrice'])
    except Exception as e:
        print(f"❌ Error fetching CMP for {symbol}: {e}")
        return None

# Get 52-week high/low
def get_52_week_range(symbol):
    try:
        session.get("https://www.nseindia.com", timeout=5)
        url = get_nse_equity_url(symbol)
        response = session.get(url, timeout=5)
        data = response.json()
        low = float(data['priceInfo']['weekLow'])
        high = float(data['priceInfo']['weekHigh'])
        return low, high
    except Exception as e:
        print(f"❌ Error fetching 52-week range for {symbol}: {e}")
        return None, None

# Get traded volume
def get_volume_data(symbol):
    try:
        session.get("https://www.nseindia.com", timeout=5)
        url = get_nse_equity_url(symbol)
        response = session.get(url, timeout=5)
        data = response.json()
        volume = data['priceInfo'].get('totalTradedVolume', 0)
        return int(volume)
    except Exception as e:
        print(f"❌ Error fetching volume data for {symbol}: {e}")
        return None
