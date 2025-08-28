from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import Currency, CurrencyDetail
from app.db import store

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("", response_model=List[Currency])
def list_currencies():
    return store.get_currency_list()


@router.get("/{currency_id}", response_model=CurrencyDetail)
def get_currency(currency_id: str):
    detail = store.get_currency_detail(currency_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Currency not found")
    return detail
