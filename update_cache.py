# update_cache.py

import os
import json
import requests
from bs4 import BeautifulSoup

SYMBOLS_FILE = os.path.join("symbols", "nse_symbols.json")
CACHE_PATH = os.path.join("data", "screener_cache.json")

def fetch_earnings(stock_name):
    url = f"https://www.screener.in/company/{stock_name}/consolidated/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "ranges-table"})

        if not table:
            return None

        rows = table.find_all("tr")
        labels = [td.text.strip() for td in rows[0].find_all("td")]
        data = [td.text.strip().replace(",", "") for td in rows[1].find_all("td")]

        try:
            rev_index = labels.index("Sales")
            pat_index = labels.index("Net Profit")

            revenue = data[rev_index] + " Cr"
            pat = data[pat_index] + " Cr"
            profit_growth = data[pat_index + 1] + "%"

            return f"• Revenue: ₹{revenue}\n• PAT: ₹{pat}\n• YoY Profit Growth: {profit_growth}"
        except:
            return None

    except Exception as e:
        print(f"Error fetching {stock_name}: {e}")
        return None

def load_symbols():
    try:
        with open(SYMBOLS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [entry["symbol"].upper() for entry in data if "symbol" in entry]
    except Exception as e:
        print(f"⚠️ Failed to load symbols: {e}")
        return []

def update_cache(symbols):
    if not os.path.exists("data"):
        os.makedirs("data")

    cache = {}
    for symbol in symbols:
        print(f"🔍 Fetching {symbol}...")
        earnings = fetch_earnings(symbol)
        if earnings:
            cache[symbol] = earnings

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

    print("\n✅ Screener cache updated successfully!")

if __name__ == "__main__":
    stock_list = load_symbols()
    if not stock_list:
        print("⚠️ No symbols found to fetch.")
    else:
        update_cache(stock_list[:50])  # Limit to 50 for initial run, or remove [:50] for full
