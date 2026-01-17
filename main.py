import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ChatMemberHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["CIT_TOKEN"]

WELCOME_TEXT = "Welcome to the channel! 🚀"
DELETE_AFTER_SECONDS = 10


# -------- /start command --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ cit-bot is running")


# -------- welcome handler --------
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member
    chat = chat_member.chat
    user = chat_member.new_chat_member.user

    # Trigger ONLY when user actually joins
    if (
        chat_member.old_chat_member.status in ("left", "kicked")
        and chat_member.new_chat_member.status == "member"
    ):
        name = user.mention_html()

        msg = await context.bot.send_message(
            chat_id=chat.id,
            text=f"👋 Welcome {name}\n\n{WELCOME_TEXT}",
            parse_mode="HTML",
        )

        await asyncio.sleep(DELETE_AFTER_SECONDS)
        await msg.delete()


# -------- main --------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    print("✅ CIT BOT STARTED (POLLING MODE)")
    app.run_polling()


if __name__ == "__main__":
    main()
