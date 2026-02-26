import feedparser
import schedule
import time
from telegram import Bot

TOKEN = "8745648926:AAGvfNOuDUNkpRhhXE_UEef4nbKMbnVbuYc"
CHAT_ID = -1003841593986
TOPIC_ID = 2

bot = Bot(token=TOKEN)

def send_crypto_news():
    url = "https://feeds.feedburner.com/CoinDesk"
    feed = feedparser.parse(url)

    for entry in feed.entries[:3]:
        message = f"📰 {entry.title}\n{entry.link}"
        bot.send_message(chat_id=CHAT_ID, text=message, message_thread_id=TOPIC_ID)

send_crypto_news()
schedule.every(60).minutes.do(send_crypto_news)

print("Bot lancé...")

while True:
    schedule.run_pending()
    time.sleep(1)