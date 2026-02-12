import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from supabase import create_client

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет 👋 Я бот для управления датами площадок.\n\nКоманды:\n/addvenue\n/adddates\n/getdates")


@dp.message(Command("addvenue"))
async def add_venue(message: types.Message):
    try:
        _, name, country, city, capacity = message.text.split(",")
        response = supabase.table("venues").insert({
            "name": name.strip(),
            "country": country.strip(),
            "city": city.strip(),
            "capacity": int(capacity.strip())
        }).execute()

        await message.answer(f"✅ Площадка {name} добавлена")
    except:
        await message.answer("Формат:\n/addvenue, Название, Страна, Город, Вместимость")


@dp.message(Command("adddates"))
async def add_dates(message: types.Message):
    try:
        _, venue_name, month, year, dates = message.text.split(",")
        venue = supabase.table("venues").select("*").eq("name", venue_name.strip()).execute()

        if not venue.data:
            await message.answer("❌ Площадка не найдена")
            return

        venue_id = venue.data[0]["id"]

        supabase.table("availability").insert({
            "venue_id": venue_id,
            "month": int(month.strip()),
            "year": int(year.strip()),
            "free_dates": dates.strip()
        }).execute()

        await message.answer("✅ Даты добавлены")
    except:
        await message.answer("Формат:\n/adddates, Название, Месяц(число), Год, 1-5,10,15")


@dp.message(Command("getdates"))
async def get_dates(message: types.Message):
    try:
        _, venue_name, month, year = message.text.split(",")

        venue = supabase.table("venues").select("*").eq("name", venue_name.strip()).execute()

        if not venue.data:
            await message.answer("❌ Площадка не найдена")
            return

        venue_id = venue.data[0]["id"]

        data = supabase.table("availability")\
            .select("*")\
            .eq("venue_id", venue_id)\
            .eq("month", int(month.strip()))\
            .eq("year", int(year.strip()))\
            .execute()

        if not data.data:
            await message.answer("Нет данных")
            return

        dates = data.data[0]["free_dates"]
        await message.answer(f"📅 Свободные даты:\n{dates}")

    except:
        await message.answer("Формат:\n/getdates, Название, Месяц(число), Год")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
