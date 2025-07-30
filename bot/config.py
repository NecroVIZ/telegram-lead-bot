import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()] or [int(os.getenv("ADMIN_ID"))] if os.getenv("ADMIN_ID") else []
GOOGLE_CREDS_PATH = os.getenv("GOOGLE_CREDS_PATH", "creds.json")