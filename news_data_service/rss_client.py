import feedparser
from datetime import datetime

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss"
]

def fetch_rss_news() -> list:
    news = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:  # limit latest 10
                news.append({
                    "title": entry.get("title"),
                    "url": entry.get("link"),
                    "source": feed.feed.get("title"),
                    "published_at": datetime(*entry.published_parsed[:6])
                })
        except Exception as e:
            print(f"[RSS] Error fetching {url}: {e}")
    return news
