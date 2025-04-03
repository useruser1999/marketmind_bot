# bot.py
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from fastapi import FastAPI, Request
import uvicorn
import os
import openai
from datetime import datetime

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- DB INIT ---
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    is_pro BOOLEAN DEFAULT 0
)''')
conn.commit()

# --- LOG ADMIN ACTIONS ---
def log_admin_action(admin_id: int, action: str):
    try:
        with open("admin.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] Admin {admin_id}: {action}\n")
    except Exception as e:
        return str(e)
    return None

# --- Inline Keyboard for subscription ---
payment_keyboard = InlineKeyboardMarkup(row_width=1)
payment_keyboard.add(
    InlineKeyboardButton("💳 Оплатить подписку (карты UA, EU, СНГ)", url="https://www.wayforpay.com/link/yourpaymentlink")
)

# команды администратора
# (оставляем только начало — остальное подгрузим динамически в следующем шаге)
