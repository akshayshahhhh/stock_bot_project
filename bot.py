# bot.py

import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from handlers.message_handler import handle_stock_query

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Replace this with your actual token
BOT_TOKEN = "7844949436:AAGuSSKfIaxojLMCcoWT2gigrq7ofv06zyQ"

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_stock_query))

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
