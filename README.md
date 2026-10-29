# Price Alert Scraper



A Python web scraper that checks a book's price and sends a Telegram message when the price changes.



## Features



- Scrapes the book price with Requests and BeautifulSoup

- Saves the last checked price locally

- Sends change alerts through a Telegram bot

- Can run automatically with Windows Task Scheduler



## Setup



Install the required packages:



```bash

pip install requests beautifulsoup4 python-dotenv

