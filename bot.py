import os
import asyncio
import requests
from urllib.parse import urlparse, parse_qs, quote
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "https://tg-init-backend.onrender.com")
TON_RECEIVER = os.getenv("TON_RECEIVER", "EQXXXXXXXXXXXXXXXXXXXXXXXXXXXX")  # your wallet

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def handle_start(message: types.Message):
    await message.answer("Send me a Stickerdom URL with initData to continue.")

@dp.message()
async def handle_any_message(message: types.Message):
    text = message.text.strip()
    
    try:
        url = urlparse(text)
        if "stickerdom.store" not in url.netloc:
            await message.answer("❌ Invalid URL.")
            return
        
        query = parse_qs(url.query)
        init_data = query.get("initData", [None])[0]
        if not init_data:
            await message.answer("❌ No initData found in URL.")
            return

        resp = requests.post(f"{BACKEND_URL}/validate-initdata", json={"initData": init_data})
        if resp.status_code != 200:
            await message.answer("❌ initData is invalid or expired.")
            return

        parts = url.path.strip("/").split("/")
        if len(parts) >= 3:
            bundle_id = parts[1]
            pack_id = parts[2]
        else:
            bundle_id = "unknown"
            pack_id = "0"

        amount_ton = 1.5
        comment = f"bundle:{bundle_id}-pack:{pack_id}"
        comment_encoded = quote(comment)

        payment_url = f"https://app.tonkeeper.com/transfer/{TON_RECEIVER}?amount={amount_ton}&text={comment_encoded}"

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"💸 Pay {amount_ton} TON", url=payment_url)]
            ]
        )

        await message.answer(
            f"✅ initData validated.\n\nClick below to buy Sticker Pack <b>{bundle_id}/{pack_id}</b>:",
            reply_markup=keyboard
        )

    except Exception as e:
        await message.answer(f"❌ Error: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
