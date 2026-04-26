import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import firebase_admin
from firebase_admin import credentials, db

# ------------------ LOGGING ------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ------------------ FIREBASE SETUP ------------------
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-irrigation-9f1bd-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# ------------------ TELEGRAM TOKEN ------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise Exception("TOKEN not found in environment variables")

# ------------------ FLASK APP ------------------
flask_app = Flask(__name__)

# ------------------ TELEGRAM APP ------------------
tg_app = ApplicationBuilder().token(TOKEN).build()

# ------------------ COMMANDS ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱🤖 Smart Irrigation Bot Activated!\n\n"
        "Use /status /motor_on /motor_off 🌾"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = db.reference('/')
    data = ref.get() or {}

    moisture = data.get("soil_moisture", "No data")
    motor = data.get("motor", "Unknown")

    await update.message.reply_text(
        f"📊 Live Status\n\n"
        f"🌱 Soil Moisture: {moisture}\n"
        f"💧 Motor: {motor}"
    )

async def motor_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.reference('/').update({"motor": "ON"})
    await update.message.reply_text("💧 Motor ON")

async def motor_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.reference('/').update({"motor": "OFF"})
    await update.message.reply_text("🛑 Motor OFF")

# ------------------ REGISTER HANDLERS ------------------
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("status", status))
tg_app.add_handler(CommandHandler("motor_on", motor_on))
tg_app.add_handler(CommandHandler("motor_off", motor_off))

# ------------------ WEBHOOK ROUTE ------------------
@flask_app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), tg_app.bot)
    await tg_app.process_update(update)
    return "ok"

# ------------------ SET WEBHOOK ON START ------------------
@app.post_init
async def on_startup(application):
    webhook_url = os.environ.get("WEB")

    if not webhook_url:
        raise Exception("WEBHOOK_URL not set")

    await application.bot.set_webhook(
        url=f"{webhook_url}/{TOKEN}"
    )

# ------------------ RUN FLASK ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
