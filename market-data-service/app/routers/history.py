from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import HistoryCandle
from app.db import store

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{currency_id}", response_model=List[HistoryCandle])
def get_history(currency_id: str):
    candles = store.get_history(currency_id)
    if not candles:
        raise HTTPException(status_code=404, detail="No history found for currency")
    return candles
