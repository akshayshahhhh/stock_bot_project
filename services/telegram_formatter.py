from datetime import datetime

def format_report_for_telegram(report):
    if not report or not isinstance(report, dict):
        return "⚠️ Error: Invalid stock report data."

    def fmt(val):
        return f"{val:.2f}" if isinstance(val, float) else val

    date_str = datetime.now().strftime("%Y-%m-%d")
    msg = f"""📘 {report['symbol']} – TECHNICAL & FUNDAMENTAL SNAPSHOT
Date: {date_str}

I. PRICE SUMMARY
• CMP: ₹{fmt(report['price'])}
• 52-Week Range: ₹{report['low']} – ₹{report['high']}
• Trend: {report['trend']}
• Support Zone: {report['support_zone']}
• Resistance Zone: {report['resistance_zone']}

II. PRICE ACTION
• Candlestick Pattern: {report['candlestick']}
• Price Structure (Daily): {report['structure_daily']}
• Price Structure (Weekly): {report['structure_weekly']}
• Breakout Signal: {report['breakout_signal']}

III. VOLUME ANALYSIS
• Today’s Volume: {round(report['volume'] / 100000, 2)} Lakh
• 50-Day Avg Volume: {round(report['volume_avg'] / 100000, 2)} Lakh
• Volume Signal: {report['volume_signal']}

IV. INDICATORS
• RSI: {fmt(report['rsi'])}
• EMA 21: {fmt(report['ema_21'])}
• EMA 50: {fmt(report['ema_50'])}
• EMA 200: {fmt(report['ema_200'])}

VI. TREND & STRUCTURE
• Multi-Timeframe Trend: {report['trend']}

VII. TRADE SETUPS
• Breakout Setup: {report['breakout_signal']}

📌 Disclaimer: This analysis is for informational purposes only and should not be considered as investment advice.
"""
    return msg.strip()
