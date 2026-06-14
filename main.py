import os
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer("Salom! Valyuta kursini bilish uchun yozing:\nMasalan: USD, EUR, RUB")

@dp.message()
async def currency_handler(message: Message) -> None:
    currency = message.text.upper()
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        uzs = data['conversion_rates']['UZS']
        rub = data['conversion_rates']['RUB']
        eur = data['conversion_rates']['EUR']
        usd = data['conversion_rates']['USD']
        await message.answer(
            f"💱 1 {currency} kursi:\n"
            f"🇺🇿 UZS: {uzs:,.0f} so'm\n"
            f"🇷🇺 RUB: {rub:.2f} rubl\n"
            f"🇪🇺 EUR: {eur:.4f}\n"
            f"🇺🇸 USD: {usd:.4f}"
        )
    else:
        await message.answer("Valyuta topilmadi! Masalan: USD, EUR, RUB")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())