# from fastapi import APIRouter, HTTPException
# from typing import List
# from app.schemas import HistoryCandle
# from app.db import store

# router = APIRouter(prefix="/history", tags=["history"])


# @router.get("/{currency_id}", response_model=List[HistoryCandle])
# def get_history(currency_id: str):
#     candles = store.get_history(currency_id)
#     if not candles:
#         raise HTTPException(status_code=404, detail="No history found for currency")
#     return candles

# from fastapi import APIRouter, HTTPException
# import httpx
# from app.config import ROOT_URL, API_KEY_HEADER

# router = APIRouter(
#     prefix="/history",
#     tags=["history"]
# )

# @router.get("/{coin_id}")
# async def get_coin_history(coin_id: str, vs_currency: str = "usd", days: int = 30):
#     """
#     Get historical price chart data for a coin
#     Example: /history/bitcoin?vs_currency=usd&days=30
#     """
#     url = f"{ROOT_URL}/coins/{coin_id}/market_chart"
#     params = {"vs_currency": vs_currency, "days": days}

#     async with httpx.AsyncClient() as client:
#         resp = await client.get(url, params=params, headers=API_KEY_HEADER)

#     if resp.status_code != 200:
#         raise HTTPException(status_code=resp.status_code, detail="Error fetching history")

#     return resp.json()

# app/routers/history.py
from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.db import store
from app.schemas import HistoryCandle

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{currency_id}", response_model=List[HistoryCandle])
def get_history(currency_id: str, days: int = Query(7, ge=1, le=365)):
    history = store.get_history(currency_id, days=days)
    if not history:
        raise HTTPException(status_code=404, detail="No history found")
    return history
