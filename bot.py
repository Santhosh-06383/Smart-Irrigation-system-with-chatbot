import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import firebase_admin
from firebase_admin import credentials, db

# ------------------ FIREBASE SETUP ------------------

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-irrigation-9f1bd-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# ------------------ TELEGRAM BOT ------------------

TOKEN = "8158459010:AAF2C_EzPT1hcqLksuiynCY0Ur3ndK9KayI"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ------------------ COMMANDS ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """🌱🤖 (Anto, Santo, Veera)'s Smart Irrigation Bot Activated! 💧

Welcome! Your irrigation system is now connected.

Use:
👉 /status - Check soil & pump status
👉 /motor_on - Turn ON motor
👉 /motor_off - Turn OFF motor

Happy Farming 🌾😊""")

# Read soil moisture
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = db.reference('/')
    data = ref.get()

    moisture = data.get("soil_moisture", "No data")
    motor = data.get("motor", "Unknown")

    await update.message.reply_text(
  f"""📊 Live Status

🌱 Soil Moisture: {moisture}
💧 Motor Status: {motor}

System working perfectly ✅"""
    )

# Turn motor ON
async def motor_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = db.reference('/')
    ref.update({"motor": "ON"})

    await update.message.reply_text("💧 Motor turned ON")

# Turn motor OFF
async def motor_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ref = db.reference('/')
    ref.update({"motor": "OFF"})

    await update.message.reply_text("🛑 Motor turned OFF")

# ------------------ MAIN FUNCTION ------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("motor_on", motor_on))
    app.add_handler(CommandHandler("motor_off", motor_off))

    print("🚀 Bot is running🌳.....")
    app.run_polling()

if __name__ == "__main__":
    main()
