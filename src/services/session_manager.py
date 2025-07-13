# src/services/session_manager.py

from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID", 0))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION_NAME = "session"  # Or make dynamic if multi-user

def get_client():
    return TelegramClient(SESSION_NAME, API_ID, API_HASH)
