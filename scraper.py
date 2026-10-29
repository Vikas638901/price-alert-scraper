import json
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
STATE_FILE = BASE_DIR / "last_price.json"


def get_price():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0 (learning project)"},
        timeout=15,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    price_element = soup.select_one(".price_color")

    if price_element is None:
        raise ValueError("Price nahi mila.")

    match = re.search(r"\d+(?:\.\d{1,2})?", price_element.get_text())

    if match is None:
        raise ValueError("Price number nahi mila.")

    return "GBP " + match.group()


def load_old_price():
    if not STATE_FILE.exists():
        return None

    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return data.get("price")


def save_price(price):
    STATE_FILE.write_text(
        json.dumps({"price": price}, indent=2),
        encoding="utf-8",
    )


def send_telegram(message):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not token or not chat_id:
        raise ValueError(".env mein BOT_TOKEN aur CHAT_ID dono chahiye.")

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": message},
        timeout=15,
    )
    response.raise_for_status()

    if not response.json().get("ok"):
        raise RuntimeError("Telegram alert nahi bheja ja saka.")


def main():
    current_price = get_price()
    old_price = load_old_price()

    print("Abhi ka price:", current_price)

    if old_price is None:
        print("Pehli baar check kiya; current price save kar diya.")
    elif current_price != old_price:
        message = (
            "Price change alert!\n"
            f"Book: A Light in the Attic\n"
            f"Purana price: {old_price}\n"
            f"Naya price: {current_price}\n"
            f"Link: {URL}"
        )
        send_telegram(message)
        print("Price change ka Telegram alert bhej diya.")
    else:
        print("Price mein koi change nahi.")

    save_price(current_price)


if __name__ == "__main__":
    main()