# bot.py

import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from handlers.message_handler import handle_stock_query
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Load token securely or directly
BOT_TOKEN = "7844949436:AAGuSSKfIaxojLMCcoWT2gigrq7ofv06zyQ"  # Already in your working version

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_stock_query))

    # Optional scheduler (enabled if you use any scheduled tasks)
    scheduler = AsyncIOScheduler()
    scheduler.start()

    logger.info("Application started")
    app.run_polling()

if __name__ == "__main__":
    main()
