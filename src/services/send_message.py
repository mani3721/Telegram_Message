# send_message.py

from telethon import TelegramClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID") or 0)
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH") or ""

async def send_to_chat(chat_id: int, message: str):
    client = TelegramClient("session", TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()

    await client.send_message(chat_id, message)
    print(f"✅ Message sent to {chat_id}")
    await client.disconnect()