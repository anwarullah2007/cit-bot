import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["CIT_TOKEN"]

WELCOME_TEXT = "Welcome to the group! 🚀"
DELETE_AFTER_SECONDS = 10


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🟢 /start received")
    await update.message.reply_text("✅ Bot is running")


# ---------- welcome via NEW_CHAT_MEMBERS ----------
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔔 NEW_CHAT_MEMBERS event received")

    for user in update.message.new_chat_members:
        print(f"👤 New user joined: {user.id}")

        name = user.mention_html()

        msg = await update.message.reply_html(
            f"👋 Welcome {name}\n\n{WELCOME_TEXT}"
        )

        print("🕒 Waiting before deleting welcome message")
        await asyncio.sleep(DELETE_AFTER_SECONDS)

        await msg.delete()
        print("🗑️ Welcome message deleted")


# ---------- main ----------
def main():
    print("🚀 Starting bot in polling mode")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
    )

    print("✅ Bot polling started")
    app.run_polling()


if __name__ == "__main__":
    main()
