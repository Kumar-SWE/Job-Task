import os
import requests
from datetime import datetime

API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "17461630679090c30081a1b6d8a24a0f11ea25dd")  # put your key here or set in env
BASE_URL = "https://cryptopanic.com/api/developer/v2/posts/"

def fetch_crypto_news(filter='public', kind='news') -> list:
    params = {
        "auth_token": API_KEY,
        "filter": filter,
        "kind": kind
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        news = []
        for item in data.get("results", []):
            news.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "source": item.get("source", {}).get("title"),
                "published_at": datetime.strptime(item.get("published_at")[:19], "%Y-%m-%dT%H:%M:%S")
            })
        return news
    except Exception as e:
        print(f"[CryptoPanic] Error fetching news: {e}")
        return []
