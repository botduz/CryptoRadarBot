import os
import asyncio
import feedparser
from telegram import Bot

BOT_TOKEN = os.environ["TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
TOPIC_ID = int(os.environ.get("TOPIC_ID", "0"))
INTERVAL_MIN = int(os.environ.get("INTERVAL_MIN", "60"))

bot = Bot(token=BOT_TOKEN)

FEEDS = [
    ("CoinDesk", "https://feeds.feedburner.com/CoinDesk"),
    ("Cointelegraph", "https://cointelegraph.com/rss"),
]

def get_news(max_items=4):
    msgs = []
    for name, url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:2]:
            msgs.append(f"📰 [{name}] {entry.title}\n{entry.link}")
    return msgs[:max_items]

async def send_once():
    kwargs = {}
    if TOPIC_ID != 0:
        kwargs["message_thread_id"] = TOPIC_ID
    for msg in get_news():
        await bot.send_message(chat_id=CHAT_ID, text=msg, **kwargs)
        await asyncio.sleep(1)

async def main():
    print("Bot en ligne 24/7")
    await send_once()
    while True:
        await asyncio.sleep(INTERVAL_MIN * 60)
        await send_once()

if __name__ == "__main__":
    asyncio.run(main())
