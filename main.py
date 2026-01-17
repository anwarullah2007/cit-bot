import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler,
)

BOT_TOKEN = os.environ["BOT_TOKEn"]

WELCOME_TEXT = "Welcome to the channel! 🚀"

# -------- HANDLERS --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ cit-bot is running")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member.new_chat_member
    if member.status == "member":
        user = member.user
        name = user.mention_html()

        msg = await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=f"👋 Welcome {name}\n\n{WELCOME_TEXT}",
            parse_mode="HTML"
        )

        await asyncio.sleep(10)
        await msg.delete()

# -------- MAIN --------

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))

    print("✅ CIT BOT STARTED (POLLING MODE)")
    app.run_polling()

if __name__ == "__main__":
    main()
