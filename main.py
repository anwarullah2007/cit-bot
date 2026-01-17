import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["CIT_TOKEN"]

async def debug_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 UPDATE RECEIVED:")
    print(update)

def main():
    print("🚀 Bot started")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, debug_all))
    app.run_polling()

if __name__ == "__main__":
    main()
