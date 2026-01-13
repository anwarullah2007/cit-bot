import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ChatMemberHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("CIT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

WELCOME_TEXT = "Welcome {username} 👋"
DELETE_AFTER = 10

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()


# ---- /start COMMAND ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ cit-bot is running")


# ---- WELCOME HANDLER ----
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
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "OK"


if __name__ == "__main__":
    asyncio.run(application.initialize())
    asyncio.run(application.start())
    print("✅ cit-bot webhook started")
    app.run(host="0.0.0.0", port=PORT)
