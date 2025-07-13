# get_chats.py

from telethon import TelegramClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID") or 0)
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH") or ""

async def get_chat_list():
    client = TelegramClient("session", TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()

    result = []
    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        if dialog.is_group:
            chat_type = "Group"
        elif dialog.is_channel:
            chat_type = "Channel"
        elif dialog.is_user and getattr(entity, "bot", False):
            chat_type = "Bot"
        else:
            continue

        result.append({
            "type": chat_type,
            "name": dialog.name,
            "chat_id": dialog.id
        })

    await client.disconnect()
    return result


