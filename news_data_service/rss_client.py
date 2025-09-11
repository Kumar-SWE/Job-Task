# import feedparser
# from datetime import datetime

# RSS_FEEDS = [
#     "https://www.coindesk.com/arc/outboundfeeds/rss/",
#     "https://cointelegraph.com/rss"
# ]

# def fetch_rss_news() -> list:
#     news = []
#     for url in RSS_FEEDS:
#         try:
#             feed = feedparser.parse(url)
#             for entry in feed.entries[:10]:  # limit latest 10
#                 news.append({
#                     "title": entry.get("title"),
#                     "url": entry.get("link"),
#                     "source": feed.feed.get("title"),
#                     "published_at": datetime(*entry.published_parsed[:6])
#                 })
#         except Exception as e:
#             print(f"[RSS] Error fetching {url}: {e}")
#     return news


import feedparser
from datetime import datetime
from typing import List, Dict

RSS_FEEDS = {
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "cointelegraph": "https://cointelegraph.com/rss"
}

def fetch_rss_news(feed_name: str = "coindesk", limit: int = 10) -> List[Dict]:
    url = RSS_FEEDS.get(feed_name)
    if not url:
        return []

    feed = feedparser.parse(url)
    news = []
    for entry in feed.entries[:limit]:
        published = getattr(entry, "published", getattr(entry, "updated", None))
        if published:
            try:
                published_dt = datetime(*entry.published_parsed[:6])
            except Exception:
                published_dt = None
        else:
            published_dt = None

        news.append({
            "title": entry.get("title"),
            "url": entry.get("link"),
            "source": feed_name,
            "published_at": published_dt
        })
    return news
