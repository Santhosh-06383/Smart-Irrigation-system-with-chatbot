import os
import logging
import asyncio

from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import firebase_admin
from firebase_admin import credentials, db

# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==================================================
# FIREBASE SETUP
# ==================================================

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smart-irrigation-9f1bd-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# ==================================================
# ENV VARIABLES
# ==================================================

TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN:
    raise Exception("TELEGRAM_TOKEN not found in environment variables")

if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL not found in environment variables")

# ==================================================
# FLASK APP
# ==================================================

flask_app = Flask(__name__)

# ==================================================
# TELEGRAM APP
# ==================================================

tg_app = ApplicationBuilder().token(TOKEN).build()

# ==================================================
# COMMANDS
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """🌱🤖 Smart Irrigation Bot Activated!

Use:
👉 /status
👉 /motor_on
👉 /motor_off

Happy Farming 🌾"""
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = db.reference("/")
    data = ref.get() or {}

    moisture = data.get("soil_moisture", "No data")
    motor = data.get("motor", "Unknown")

    await update.message.reply_text(
        f"""📊 Live Status

🌱 Soil Moisture: {moisture}
💧 Motor: {motor}"""
    )


async def motor_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.reference("/").update({"motor": "ON"})
    await update.message.reply_text("💧 Motor ON")


async def motor_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.reference("/").update({"motor": "OFF"})
    await update.message.reply_text("🛑 Motor OFF")


# ==================================================
# REGISTER HANDLERS
# ==================================================

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("status", status))
tg_app.add_handler(CommandHandler("motor_on", motor_on))
tg_app.add_handler(CommandHandler("motor_off", motor_off))

# ==================================================
# FLASK ROUTES
# ==================================================

@flask_app.route("/")
def home():
    return "Smart Irrigation Bot Running ✅"


@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), tg_app.bot)
    asyncio.run(tg_app.process_update(update))
    return "ok"


# ==================================================
# STARTUP
# ==================================================

async def startup():
    await tg_app.initialize()
    await tg_app.start()

    await tg_app.bot.set_webhook(
        url=f"{WEBHOOK_URL}/{TOKEN}"
    )

    print("✅ Webhook connected")


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    asyncio.run(startup())

    print("🚀 Smart Irrigation Bot Running")

    flask_app.run(host="0.0.0.0", port=PORT)
