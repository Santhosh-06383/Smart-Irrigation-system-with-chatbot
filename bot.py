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
# ENV VARIABLES
# ==================================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN:
    raise Exception("TELEGRAM_TOKEN not found")

if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL not found")

# ==================================================
# FIREBASE SETUP
# ==================================================
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://smart-irrigation-9f1bd-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# ==================================================
# FLASK APP
# ==================================================
flask_app = Flask(__name__)

# ==================================================
# TELEGRAM BOT
# ==================================================
tg_app = ApplicationBuilder().token(TOKEN).build()

# ==================================================
# COMMANDS
# ==================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """🌱🤖 Smart Irrigation Bot Activated
    
Created by : Antony, Santhosh, Veera.
Guided by  : Dr.T.Rakesh,ASP/EEE.

Welcome! Your irrigation system is connected.

Use:
👉 /status
👉 /motor_on
👉 /motor_off

Happy Farming 🌾😊"""
    )


# ==================================================
# FIXED ONLY WHERE NEEDED (STATUS)
# ==================================================
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ref = db.reference("/")

        data = ref.get()

        print("RAW FIREBASE DATA:", data)  # 👈 IMPORTANT DEBUG

        if not data:
            raise Exception("No data received from Firebase")

        moisture = data.get("soil_moisture", "No data")
        motor = data.get("motor", "Unknown")
        mode = data.get("mode", "Unknown")

        await update.message.reply_text(
            f"""📊 Live Status

🌱 Soil Moisture: {moisture}
💧 Motor Status: {motor}
⚙️ Mode: {mode}

System OK ✅"""
        )

    except Exception as e:
        logging.exception(e)
        await update.message.reply_text(f"⚠️ REAL ERROR: {str(e)}")

# ==================================================
# MOTOR ON (UNCHANGED LOGIC, SAFE UPDATE)
# ==================================================
async def motor_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        db.reference("/motor").set("ON")
        await update.message.reply_text("💧 Motor turned ON")

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Failed to turn ON motor")


# ==================================================
# MOTOR OFF
# ==================================================
async def motor_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        db.reference("/motor").set("OFF")
        await update.message.reply_text("🛑 Motor turned OFF")

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Failed to turn OFF motor")


# ==================================================
# REGISTER HANDLERS
# ==================================================
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("status", status))
tg_app.add_handler(CommandHandler("motor_on", motor_on))
tg_app.add_handler(CommandHandler("motor_off", motor_off))

# ==================================================
# ROUTES
# ==================================================
@flask_app.route("/")
def home():
    return "Smart Irrigation Bot Running ✅"


@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), tg_app.bot)

        # ❗ FIX: safer Render execution (prevents random crash)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(tg_app.process_update(update))

        return "ok"

    except Exception as e:
        logging.error(e)
        return "error", 500


# ==================================================
# START TELEGRAM + WEBHOOK
# ==================================================
async def startup():
    await tg_app.initialize()
    await tg_app.start()

    await tg_app.bot.set_webhook(
        url=f"{WEBHOOK_URL}/webhook"
    )

    print("✅ Webhook Connected")
    print("🚀 Smart Irrigation Bot Running")


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(startup())

    print("🚀 Smart Irrigation Bot Running on Render")

    flask_app.run(host="0.0.0.0", port=PORT, debug=False)
