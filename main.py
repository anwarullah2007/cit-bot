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
tg_app = Application.builder().token(BOT_TOKEN).build()


# ---- TEST COMMAND ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ cit-bot is running (webhook)")


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


tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))


@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), tg_app.bot)
    tg_app.update_queue.put_nowait(update)
    return "OK"


async def init_bot():
    await tg_app.initialize()
    await tg_app.start()


if __name__ == "__main__":
    print("CIT BOT WEBHOOK STARTED")
    asyncio.run(init_bot())
    app.run(host="0.0.0.0", port=PORT)

