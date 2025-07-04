# weekly_scheduler.py

from apscheduler.schedulers.blocking import BlockingScheduler
from services.screener_fetcher import batch_update_stocks

# List of stocks to auto-refresh weekly
WATCHLIST = ["INFY", "TCS", "RELIANCE", "HDFCBANK", "ICICIBANK", "LT"]

def update_screener_weekly():
    print("🔄 Weekly Screener Cache Update Started...")
    batch_update_stocks(WATCHLIST)
    print("✅ Screener Cache Updated Successfully.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Schedule job to run every Sunday at 7 AM
    scheduler.add_job(update_screener_weekly, "cron", day_of_week="sun", hour=7, minute=0)

    print("🕒 Weekly scheduler running... Press Ctrl+C to stop.")
    scheduler.start()
