# generate_report.py

from services.analysis_engine import generate_stock_report
from services.telegram_formatter import format_stock_report

def generate_report(stock_name):
    result, err = generate_stock_report(stock_name)
    if err or result is None:
        return f"❌ Error: {err or 'Failed to generate report.'}"
    return format_stock_report(result)
