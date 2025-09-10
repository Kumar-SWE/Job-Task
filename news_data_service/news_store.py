import asyncio
from datetime import datetime
from cryptopanic_client import fetch_crypto_news
from rss_client import fetch_rss_news

class NewsStore:
    def __init__(self):
        self.news_list = []

    async def refresh_news_loop(self, interval_seconds: int = 180):
        while True:
            try:
                news = fetch_crypto_news()
                news += fetch_rss_news()
                self.news_list = news
                print(f"[NewsStore] News refreshed at {datetime.now()}, total={len(news)}")
            except Exception as e:
                print(f"[NewsStore] Error in refresh loop: {e}")
            await asyncio.sleep(interval_seconds)

store = NewsStore()
