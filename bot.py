import os
import asyncio
import requests
import urllib.parse
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
    await message.answer("Send a URL or initData string to validate.")

@dp.message()
async def handle_initdata_message(message: types.Message):
    text = message.text.strip()

    # Extract initData from URL or treat entire message as initData
    parsed = urllib.parse.urlparse(text)
    query = urllib.parse.parse_qs(parsed.query)
    init_data = query.get("initData", [text])[0]

    # Send initData to backend
    try:
        response = requests.post(f"{BACKEND_URL}/validate-initdata", json={"initData": init_data})
        if response.status_code == 200:
            data = response.json()
            await message.answer(f"✅ Validated:\n<code>{data['data']}</code>")
        else:
            await message.answer(f"❌ Invalid:\n<code>{response.text}</code>")
    except Exception as e:
        await message.answer(f"🚨 Error:\n<code>{str(e)}</code>")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
