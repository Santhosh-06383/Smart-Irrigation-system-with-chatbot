import os
import logging
from flask import Flask, request

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- LOGGING ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------- TOKEN (USE ENV ON RENDER) ----------------
TOKEN = os.getenv("8158459010:AAF2C_EzPT1hcqLksuiynCY0Ur3ndK9KayI")

# Render URL example:
# https://your-service.onrender.com/webhook
WEBHOOK_URL = os.getenv("https://Smart-Irrigation-system-with-chatbot.onrender.com/webhook")

# ---------------- TELEGRAM HANDLERS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱🤖 *(Anto, Santo, Veera)'s Smart Irrigation Bot Activated!* 💧\n\n"
        "Welcome! Your irrigation system is now connected.\n\n"
        "Use:\n"
        "👉 /status - Check soil & pump status\n\n"
        "Happy Farming 🌾😊",
        parse_mode="Markdown"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    moisture = "50%"   # later replace with Firebase
    pump = "OFF"

    await update.message.reply_text(
        f"📊 *Live Status*\n\n"
        f"🌱 Soil Moisture: {moisture}\n"
        f"🚿 Pump Status: {pump}\n\n"
        f"System working perfectly ✅",
        parse_mode="Markdown"
    )

# ---------------- TELEGRAM APP ----------------
tg_app = ApplicationBuilder().token(TOKEN).build()

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("status", status))

# ---------------- FLASK APP ----------------
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "🌱 Smart Irrigation Bot Running"

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    tg_app.update_queue.put_nowait(update)
    return "OK"

# ---------------- SET WEBHOOK ----------------
async def set_webhook():
    await tg_app.bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to: {WEBHOOK_URL}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    import asyncio

    async def main():
        await set_webhook()

        tg_app.initialize()
        tg_app.start()

        port = int(os.environ.get("PORT", 10000))
        flask_app.run(host="0.0.0.0", port=port)

    asyncio.run(main())

if __name__ == "__main__":
    main()
