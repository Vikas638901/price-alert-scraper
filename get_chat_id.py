import os

import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")

if not token:
    raise ValueError(".env file mein BOT_TOKEN nahi mila.")

response = requests.get(
    f"https://api.telegram.org/bot{token}/getUpdates",
    timeout=15,
)
response.raise_for_status()

updates = response.json()["result"]

if not updates:
    print("Telegram bot chat mein /start bhejo, phir script dobara chalao.")
else:
    for update in updates:
        message = update.get("message", {})
        chat = message.get("chat", {})
        if chat.get("id"):
            print("Chat ID:", chat["id"])