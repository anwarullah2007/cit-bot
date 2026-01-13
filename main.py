import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    ChatMemberHandler,
    ContextTypes,
    CommandHandler,
)

print("CIT BOT CODE STARTING...")

BOT_TOKEN = os.getenv("CIT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

WELCOME_TEXT = "Welcome {username} 👋\nPlease read the rules and enjoy!"
DELETE_AFTER = 10  # seconds


# ---- TEST COMMAND (CONFIRMS BOT IS RUNNING) ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ cit-bot is running")


# ---- WELCOME HANDLER ----
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member

    if chat_member.new_chat_member.status == "member":
        user = chat_member.new_chat_member.user
        username = f"@{user.username}" if user.username else user.first_name

        msg = await context.bot.send_message(
            chat_id=chat_member.chat.id,
            text=WELCOME_TEXT.format(username=username)
        )

        await asyncio.sleep(DELETE_AFTER)
        await msg.delete()


def main():
    print("CIT BOT RUNNING...")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    app.run_polling()


if __name__ == "__main__":
    main()
