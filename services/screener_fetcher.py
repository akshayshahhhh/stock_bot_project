# services/screener_fetcher.py

import requests
import json
import os
from bs4 import BeautifulSoup

CACHE_FILE = os.path.join("data", "screener_cache.json")

def fetch_screener_html(stock_name):
    url = f"https://www.screener.in/company/{stock_name.upper()}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

def parse_earnings(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table.data-table tr")

    earnings_data = {
        "revenue_2021": None,
        "pat_2021": None,
        "profit_growth_2021": None,
        "revenue_2022": None,
        "pat_2022": None,
        "profit_growth_2022": None,
        "revenue_2023": None,
        "pat_2023": None,
        "profit_growth_2023": None,
    }

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 5:
            continue

        heading = cells[0].text.strip().lower()
        if "sales" in heading:
            earnings_data["revenue_2021"] = try_parse(cells[-3].text)
            earnings_data["revenue_2022"] = try_parse(cells[-2].text)
            earnings_data["revenue_2023"] = try_parse(cells[-1].text)
        elif "net profit" in heading:
            earnings_data["pat_2021"] = try_parse(cells[-3].text)
            earnings_data["pat_2022"] = try_parse(cells[-2].text)
            earnings_data["pat_2023"] = try_parse(cells[-1].text)
        elif "profit growth" in heading:
            earnings_data["profit_growth_2021"] = try_parse(cells[-3].text, pct=True)
            earnings_data["profit_growth_2022"] = try_parse(cells[-2].text, pct=True)
            earnings_data["profit_growth_2023"] = try_parse(cells[-1].text, pct=True)

    return earnings_data

def try_parse(val, pct=False):
    try:
        val = val.replace(",", "").replace("%", "").strip()
        return round(float(val), 2) if not pct else float(val)
    except:
        return None

def update_screener_cache(stock_name):
    html = fetch_screener_html(stock_name)
    if not html:
        print(f"❌ Failed to fetch data for {stock_name}")
        return

    new_data = parse_earnings(html)

    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)

    cache[stock_name.upper()] = new_data

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

    print(f"✅ Updated Screener cache for {stock_name.upper()}")

def batch_update_stocks(stock_list):
    for stock in stock_list:
        update_screener_cache(stock)
