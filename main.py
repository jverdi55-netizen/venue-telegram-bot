import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет 👋 Я бот для управления датами площадок.\n\nКоманды:\n/addvenue\n/adddates\n/getdates")


@dp.message(Command("addvenue"))
from aiogram.filters import Command
    try:
        parts = message.text.split(",")

        if len(parts) != 5:
            raise ValueError

        _, name, country, city, capacity = parts

        response = supabase.table("venues").insert({
            "name": name.strip(),
            "country": country.strip(),
            "city": city.strip(),
            "capacity": int(capacity.strip())
        }).execute()

        if response.data:
            await message.answer(f"✅ Площадка {name.strip()} добавлена")
        else:
            await message.answer("❌ Ошибка при добавлении в базу")

    except Exception as e:
        print(e)
        await message.answer(
            "Формат:\n/addvenue, Название, Страна, Город, Вместимость"
        )




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


@dp.message(Command("addvenue"))
async def add_venue(message: types.Message):
    try:
        parts = message.text.split(",")

        if len(parts) != 5:
            await message.answer("❌ Неверный формат")
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


if __name__ == "__main__":
    asyncio.run(main())
