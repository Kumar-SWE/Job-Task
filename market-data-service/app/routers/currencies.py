# from fastapi import APIRouter, HTTPException
# from typing import List
# from app.schemas import Currency, CurrencyDetail
# from app.db import store

# router = APIRouter(prefix="/currencies", tags=["currencies"])


# @router.get("", response_model=List[Currency])
# def list_currencies():
#     return store.get_currency_list()


# @router.get("/{currency_id}", response_model=CurrencyDetail)
# def get_currency(currency_id: str):
#     detail = store.get_currency_detail(currency_id)
#     if not detail:
#         raise HTTPException(status_code=404, detail="Currency not found")
#     return detail


# from fastapi import APIRouter, HTTPException
# import httpx
# from app.config import ROOT_URL, API_KEY_HEADER

# router = APIRouter(
#     prefix="/currencies",
#     tags=["currencies"]
# )

# @router.get("/")
# async def get_currencies():
#     """
#     Get list of all supported cryptocurrencies
#     """
#     url = f"{ROOT_URL}/coins/list"
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(url, headers=API_KEY_HEADER)

#     if resp.status_code != 200:
#         raise HTTPException(status_code=resp.status_code, detail="Error fetching currencies")

#     return resp.json()


# app/routers/currencies.py
from typing import List
from fastapi import APIRouter, HTTPException
from app.db import store
from app.schemas import Currency, CurrencyDetail

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("/", response_model=List[Currency])
def list_currencies():
    return store.get_currency_list()


@router.get("/{currency_id}", response_model=CurrencyDetail)
def currency_detail(currency_id: str):
    detail = store.get_currency_detail(currency_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Currency not found")
    return detail
