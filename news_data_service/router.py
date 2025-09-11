# from fastapi import APIRouter
# from news_store import store

# router = APIRouter()

# @router.get("/news")
# async def get_news():
#     return {"news": store.news_list}

from fastapi import APIRouter, Query
from news_store import store
from rss_client import fetch_rss_news

router = APIRouter()

@router.get("/news", summary="Get latest crypto news from CryptoPanic")
def get_news():
    return {"news": store.get_news()}

@router.get("/rss", summary="Get latest crypto news from RSS feeds")
def get_rss_news(feed: str = Query("coindesk", enum=["coindesk", "cointelegraph"]), limit: int = 10):
    news = fetch_rss_news(feed_name=feed, limit=limit)
    return {"news": news}
