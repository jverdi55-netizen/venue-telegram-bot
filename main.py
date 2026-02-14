import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from supabase import create_client

# --- Переменные окружения ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Инициализация ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Команда /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет 👋 Я бот для управления площадками.\n\n"
        "Команды:\n"
        "/addvenue, Название, Страна, Город, Вместимость"
    )

# --- Команда /addvenue ---
@dp.message(Command("addvenue"))
async def add_venue(message: types.Message):
    try:
        parts = message.text.split(",")

        if len(parts) != 5:
            await message.answer("❌ Формат:\n/addvenue, Название, Страна, Город, Вместимость")
            return

        _, name, country, city, capacity = parts

        response = supabase.table("venues").insert({
            "name": name.strip(),
            "country": country.strip(),
            "city": city.strip(),
            "capacity": int(capacity.strip())
        }).execute()

        print("SUPABASE RESPONSE:", response)

        if response.data:
            await message.answer(f"✅ Площадка {name.strip()} добавлена")
        else:
            await message.answer("❌ Не удалось добавить в базу")

    except Exception as e:
        print("ERROR:", e)
        await message.answer(f"❌ Ошибка: {e}")

# --- Запуск ---
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
