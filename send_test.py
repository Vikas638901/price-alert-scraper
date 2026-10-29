import os

import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not token or not chat_id:
    raise ValueError(".env mein BOT_TOKEN aur CHAT_ID dono hone chahiye.")

response = requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data={
        "chat_id": chat_id,
        "text": "Price alert bot ka test message.",
    },
    timeout=15,
)
response.raise_for_status()

result = response.json()

if not result.get("ok"):
    raise RuntimeError(result)

print("Test message Telegram par bhej diya.")