# from fastapi import APIRouter
# from datetime import datetime

# router = APIRouter(prefix="/global", tags=["global"])

# @router.get("")
# def get_global_stats():
#     return {
#         "id": "global_1",
#         "total_market_cap_inr": 200_000_000_000_000,  
#         "total_volume_inr": 5_000_000_000_000,        
#         "btc_dominance_pct": 48.2,                    
#         "updated_at": datetime.utcnow().isoformat() + "Z"
#     }

# from fastapi import APIRouter, HTTPException
# import httpx
# from app.config import ROOT_URL, API_KEY_HEADER

# router = APIRouter(
#     prefix="/global",
#     tags=["global"]
# )

# @router.get("/")
# async def get_global_stats():
#     """
#     Get global cryptocurrency market statistics
#     """
#     url = f"{ROOT_URL}/global"
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(url, headers=API_KEY_HEADER)

#     if resp.status_code != 200:
#         raise HTTPException(status_code=resp.status_code, detail="Error fetching global stats")

#     return resp.json()["data"]

# app/routers/global_stats.py
from fastapi import APIRouter
from app.db import store

router = APIRouter(prefix="/global", tags=["global"])


@router.get("/")
def get_global_stats():
    return store.get_global_stats()
