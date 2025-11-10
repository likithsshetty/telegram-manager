from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient
import os

MONGO_URI = os.environ.get('MONGO_URI')  # Your Atlas URI
DB_NAME = 'user_db'
COLLECTION_NAME = 'users'
SIGNUP_URL = os.environ.get('SIGNUP_URL')  # e.g. http://localhost:5000/signup

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
users = db[COLLECTION_NAME]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.find_one({'telegram_id': user_id})
    if user:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"You are not registered. Please sign up here: {SIGNUP_URL} {user_id}"
        )

if __name__ == "__main__":
    TOKEN = os.environ.get('TELEGRAM_TOKEN')  # Set your bot token as env variable
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
