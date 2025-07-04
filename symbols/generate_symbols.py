import pandas as pd
import json
import os
from difflib import get_close_matches

# Load CSV and save JSON (run once)
csv_path = os.path.join(os.path.dirname(__file__), "../EQUITY_L.csv")
df = pd.read_csv(csv_path)
df = df[["SYMBOL", "NAME OF COMPANY"]].dropna()

symbol_dict = dict(zip(df["SYMBOL"], df["NAME OF COMPANY"]))

# Save JSON for use in the bot
json_path = os.path.join(os.path.dirname(__file__), "nse_symbols.json")
with open(json_path, "w") as f:
    json.dump(symbol_dict, f, indent=2)

print("✅ NSE symbols saved to nse_symbols.json")


# 🧠 This function is used by the bot for fuzzy matching user inputs
def get_best_match_symbol(user_input):
    user_input = user_input.strip().upper()

    if user_input in symbol_dict:
        return user_input  # perfect match

    # Try fuzzy match
    possible_matches = get_close_matches(user_input, symbol_dict.keys(), n=1, cutoff=0.6)
    return possible_matches[0] if possible_matches else None
