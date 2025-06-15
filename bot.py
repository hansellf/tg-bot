import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
import config
import requests
import asyncio

BOT_TOKEN = config.BOT_TOKEN
BACKEND_URL = "https://tg-init-backend.onrender.com"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(commands=["start"])
async def start_handler(message: Message):
    await message.answer("Send me your Telegram initData to validate.")

@dp.message()
async def validate_initdata(message: Message):
    initData = message.text.strip()
    try:
        resp = requests.post(f"{BACKEND_URL}/validate-initdata", json={"initData": initData})
        if resp.status_code == 200:
            data = resp.json()
            await message.answer(f"InitData is valid!\n\nData: {data['data']}")
        else:
            await message.answer(f"Invalid initData: {resp.text}")
    except Exception as e:
        await message.answer(f"Error: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
