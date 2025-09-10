from fastapi import APIRouter
from news_store import store

router = APIRouter()

@router.get("/news")
async def get_news():
    return {"news": store.news_list}
