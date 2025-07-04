# services/screener_cache.py

import json
import os

# Path to cache file
CACHE_PATH = os.path.join("data", "screener_cache.json")

def get_cached_earnings_data(stock_name: str) -> dict:
    """
    Fetch earnings data (Revenue, PAT, Profit Growth) for last 3 years
    from locally cached Screener data JSON file.
    """
    stock_name = stock_name.upper()

    # If cache file doesn't exist, return empty
    if not os.path.exists(CACHE_PATH):
        return {}

    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(stock_name, {})
    except Exception as e:
        print(f"⚠️ Error reading screener cache: {e}")
        return {}
