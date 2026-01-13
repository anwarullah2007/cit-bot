import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("CIT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

WELCOME_TEXT = "Welcome {username} 👋\nEnjoy the group!"
DELETE_AFTER = 10

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()


# ---- COMMAND TO TEST BOT ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ cit-bot is running")


# ---- WELCOME MESSAGE ----
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member
    if member.new_chat_member.status == "member":
        user = member.new_chat_member.user
        username = f"@{user.username}" if user.username else user.first_name

        msg = await context.bot.send_message(
            chat_id=member.chat.id,
            text=WELCOME_TEXT.format(username=username),
        )

        await asyncio.sleep(DELETE_AFTER)
        await msg.delete()


application.add_handler(CommandHandler("start", start))
application.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))


@app.route("/", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK"


async def main():
    await application.initialize()
    await application.start()
    print("✅ cit-bot webhook started")


if __name__ == "__main__":
    asyncio.run(main())
    app.run(host="0.0.0.0", port=PORT)
