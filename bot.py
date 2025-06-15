import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "https://tg-init-backend.onrender.com")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def handle_start(message: types.Message):
    await message.answer("Send me your Telegram initData to validate.")

@dp.message()
async def handle_initdata(message: types.Message):
    init_data = message.text.strip()
    response = requests.post(f"{BACKEND_URL}/validate-initdata", json={"initData": init_data})
    if response.status_code == 200:
        result = response.json()
        await message.answer(f"✅ Valid InitData:\n<code>{result['data']}</code>")
    else:
        await message.answer(f"❌ Invalid InitData:\n<code>{response.text}</code>")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
