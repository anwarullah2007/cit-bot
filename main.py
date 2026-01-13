import os
import asyncio
from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Customize these
WELCOME_TEXT = "Welcome {username} 👋\nPlease read the rules and enjoy the channel!"
DELETE_AFTER = 10  # seconds

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member

    if result.new_chat_member.status == "member":
        user = result.new_chat_member.user
        username = f"@{user.username}" if user.username else user.first_name

        message = await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=WELCOME_TEXT.format(username=username)
        )

        await asyncio.sleep(DELETE_AFTER)
        await message.delete()

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.run_polling()

if __name__ == "__main__":
    main()
