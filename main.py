import os
import asyncio
from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes

print("BOT STARTING...")

BOT_TOKEN = os.getenv("BOT_TOKEn")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

WELCOME_TEXT = "Welcome {username} 👋"
DELETE_AFTER = 10

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status == "member":
        user = result.new_chat_member.user
        username = f"@{user.username}" if user.username else user.first_name

        msg = await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=WELCOME_TEXT.format(username=username)
        )

        await asyncio.sleep(DELETE_AFTER)
        await msg.delete()

def main():
    print("BOT RUNNING...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.run_polling()

if __name__ == "__main__":
    main()
