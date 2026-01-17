import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ChatMemberHandler,
    ContextTypes,
)

# ===== CONFIG =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
WELCOME_TEXT = "Welcome to the group! 🚀"
DELETE_AFTER_SECONDS = 10


# ===== /start command =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🟢 /start command received")
    await update.message.reply_text("✅ Bot is running correctly")


# ===== Welcome handler with DEBUG =====
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔔 CHAT MEMBER UPDATE RECEIVED")

    chat_member = update.chat_member
    chat = chat_member.chat
    user = chat_member.new_chat_member.user

    old_status = chat_member.old_chat_member.status
    new_status = chat_member.new_chat_member.status

    print(f"👤 USER: {user.id} | OLD STATUS: {old_status} → NEW STATUS: {new_status}")
    print(f"💬 CHAT: {chat.id} ({chat.title})")

    # Only when user actually joins
    if old_status in ("left", "kicked") and new_status == "member":
        print("✅ JOIN EVENT CONFIRMED — sending welcome message")

        name = user.mention_html()

        msg = await context.bot.send_message(
            chat_id=chat.id,
            text=f"👋 Welcome {name}\n\n{WELCOME_TEXT}",
            parse_mode="HTML",
        )

        print("🕒 Waiting before deleting message...")
        await asyncio.sleep(DELETE_AFTER_SECONDS)

        await msg.delete()
        print("🗑️ Welcome message deleted")

    else:
        print("⏭️ Not a join event — ignored")


# ===== MAIN =====
def main():
    print("🚀 Starting Telegram bot (Polling Mode)")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    print("✅ Bot is now polling Telegram servers")
    app.run_polling()


if __name__ == "__main__":
    main()
