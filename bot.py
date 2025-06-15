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

def decode_jwt_payload(jwt: str) -> dict | None:
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
    await message.answer("Send me a Telegram `initData` or a URL containing the `initData` parameter.")

@dp.message()
async def handle_any_message(message: types.Message):
    text = message.text.strip()

    # Try to extract initData from URL
    parsed_url = urllib.parse.urlparse(text)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    init_data = query_params.get("initData", [None])[0] or text

    # Decode the JWT payload (optional)
    decoded = decode_jwt_payload(init_data)
    if decoded:
        await message.answer(f"🔍 JWT decoded payload:\n<pre>{json.dumps(decoded, indent=2)}</pre>")

    # Send full initData to backend
    resp = requests.post(f"{BACKEND_URL}/validate-initdata", json={"initData": init_data})
    if resp.status_code == 200:
        data = resp.json()
        await message.answer(f"✅ Backend Validation Success:\n<code>{data['data']}</code>")
    else:
        await message.answer(f"❌ Backend Rejected initData:\n<code>{resp.text}</code>")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
