from fastapi import FastAPI
import asyncio
from news_store import store
from router import router

app = FastAPI(title="News Data Service", version="1.0.0")
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": " crypto news service running"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(store.refresh_news_loop(interval_seconds=180))
