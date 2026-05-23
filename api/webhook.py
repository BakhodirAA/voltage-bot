import os
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

# ── Обработчики (твой оригинальный код) ──────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Калькулятор потери напряжения ⚡\n\n"
        "Формула:\n"
        "U = 30 * I * L / S\n\n"
        "Отправь данные через пробел:\n"
        "I L S\n\n"
        "Пример:\n"
        "50 0.8 16"
    )
    await update.message.reply_text(text)

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        I, L, S = map(float, update.message.text.split())
        U = 30 * I * L / S
        result = (
            f"Результат:\n"
            f"I = {I} A\n"
            f"L = {L} км\n"
            f"S = {S} мм²\n\n"
            f"Потеря напряжения U = {U:.2f} В"
        )
        await update.message.reply_text(result)
    except:
        await update.message.reply_text(
            "Ошибка ⚠️\n"
            "Введи 3 числа через пробел:\n"
            "I L S\n\n"
            "Пример:\n"
            "50 0.8 16"
        )

# ── Обработка входящего update от Telegram ───────────────────────

async def process_update(data: dict):
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calc))
    async with app:
        update = Update.de_json(data, app.bot)
        await app.process_update(update)

# ── Vercel serverless handler ─────────────────────────────────────

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            asyncio.run(process_update(data))
        except Exception as e:
            print("Ошибка:", e)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
