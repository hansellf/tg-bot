import logging
from aiogram import Bot, Dispatcher, executor, types
import config
import requests

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

BACKEND_URL = "https://tg-init-backend.onrender.com"

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Send me your Telegram initData to validate.")

@dp.message_handler()
async def validate_initdata(message: types.Message):
    initData = message.text.strip()
    resp = requests.post(f"{BACKEND_URL}/validate-initdata", json={"initData": initData})
    if resp.status_code == 200:
        data = resp.json()
        await message.answer(f"InitData is valid!\n\nData: {data['data']}")
    else:
        await message.answer(f"Invalid initData: {resp.text}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
