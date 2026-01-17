import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_URI", "")
UI = os.getenv("UI", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
