import os  
import requests  #
from dotenv import load_dotenv 
from aiogram import Bot, Dispatcher  
from aiogram.filters import Command  
from aiogram.types import Message  

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

bot = Bot(token=TOKEN)  # ← Bot ni bu yerda yarating
dp = Dispatcher()

# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    text = "Salom bu bot orqali valyuta kurslarini bilib olishingiz mumkin. Valyuta nomini kiriting."
    await message.answer(text)

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("Sizga qanday yordam kerak")

@dp.message()
async def echo_handler(message: Message) -> None:
    currency = message.text.upper()
    response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}")
    if response.status_code == 200:
        data = response.json()
        uzs = data['conversion_rates']['UZS']
        rub = data['conversion_rates']['RUB']
        eur = data['conversion_rates']['EUR']
        usd = data['conversion_rates']['USD']
        await message.answer(f"💱 1 {currency} kursi:\n🇺🇿 UZS: {uzs:,.0f} so'm\n🇷🇺 RUB: {rub:.2f} rubl\n🇪🇺 EUR: {eur:.4f}\n🇺🇸 USD: {usd:.4f}")
    else:
        await message.answer("Valyuta nomi xato kiritildi yoki valyuta topilmadi")

# Run the bot
async def main() -> None:
    await dp.start_polling(bot)  # ← bot ni shu yerga bering

if __name__ == "__main__":
    import asyncio  # Qo'shildi (asyncio.run ishlashi uchun)
    asyncio.run(main())