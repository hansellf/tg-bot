import os
import asyncio
import requests
import urllib.parse
import base64
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "https://tg-init-backend.onrender.com")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

def add_padding(b64_string: str) -> str:
    return b64_string + "=" * (-len(b64_string) % 4)

def decode_jwt_payload(jwt: str) -> dict:
    try:
        parts = jwt.split(".")
        if len(parts) != 3:
            return None
        payload_b64 = parts[1]
        payload_bytes = base64.urlsafe_b64decode(add_padding(payload_b64))
        payload_json = payload_bytes.decode("utf-8")
        return json.loads(payload_json)
    except Exception:
        return None

@dp.message(F.text == "/start")
async def handle_start(message: types.Message):
    await message.answer("Send me your Telegram initData to validate or a URL containing `initData` parameter.")

@dp.message()
async def handle_initdata(message: types.Message):
    text = message.text.strip()
    # Detect if text is a URL with initData param
    try:
        parsed_url = urllib.parse.urlparse(text)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        init_data_from_url = query_params.get("initData", [None])[0]
    except Exception:
        init_data_from_url = None

    init_data_to_use = init_data_from_url or text

    # If we extracted initData from URL, decode and show payload
    if init_data_from_url:
        decoded = decode_jwt_payload(init_data_from_url)
        if decoded:
            pretty_json = json.dumps(decoded, indent=2)
            await message.answer(f"🔎 Decoded initData payload:\n<pre>{pretty_json}</pre>")
        else:
            await message.answer("⚠️ Failed to decode initData payload.")
        return

    # Else fallback to your backend validation
    response = requests.post(f"{BACKEND_URL}/validate-initdata", json={"initData": init_data_to_use})
    if response.status_code == 200:
        result = response.json()
        await message.answer(f"✅ Valid InitData:\n<code>{result['data']}</code>")
    else:
        await message.answer(f"❌ Invalid InitData:\n<code>{response.text}</code>")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
