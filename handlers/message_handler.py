from telegram import Update
from telegram.ext import ContextTypes
from services.analysis_engine import generate_stock_report
from services.telegram_formatter import format_report_for_telegram
import logging

logger = logging.getLogger(__name__)

async def handle_stock_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = update.message.text.strip().upper()

        # Fetch report
        data, error = generate_stock_report(symbol)
        if error:
            await update.message.reply_text(f"❌ Error: {error}")
            return

        # Format for Telegram
        message = format_report_for_telegram(data)
        await update.message.reply_text(message, parse_mode="HTML")

        # PDF functionality is disabled for now
        # from services.pdf_generator import create_pdf_report
        # pdf_file_path = create_pdf_report(data)
        # context.bot.send_document(chat_id=update.effective_chat.id, document=open(pdf_file_path, "rb"))

    except Exception as e:
        logger.exception("🔥 EXCEPTION CAUGHT!")
        await update.message.reply_text(f"🔥 EXCEPTION CAUGHT!\n{e}")
