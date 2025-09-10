# from fastapi import APIRouter, Query
# from typing import List
# from app.schemas import PricesResponse
# from app.db import store

# router = APIRouter(prefix="/prices", tags=["prices"])


# @router.get("", response_model=PricesResponse)
# def get_prices(
#     ids: List[str] = Query(..., description="Comma-separated currency ids e.g. ids=bitcoin,ethereum"),
#     fiat: str = Query("inr"),
# ):
#     if fiat.lower() != "inr":
        
#         return {}

   
#     normalized_ids: List[str] = []
#     for part in ids:
#         normalized_ids.extend([x.strip() for x in part.split(",") if x.strip()])

#     data = store.get_prices(normalized_ids)

#     return data 



# from fastapi import APIRouter, HTTPException
# import httpx
# from app.config import ROOT_URL, API_KEY_HEADER

# router = APIRouter(
#     prefix="/prices",
#     tags=["prices"]
# )

# @router.get("/{coin_id}")
# async def get_price(coin_id: str, vs_currency: str = "usd"):
#     """
#     Get real-time price of a cryptocurrency by ID
#     Example: /prices/bitcoin?vs_currency=usd
#     """
#     url = f"{ROOT_URL}/simple/price"
#     params = {"ids": coin_id, "vs_currencies": vs_currency}

#     async with httpx.AsyncClient() as client:
#         resp = await client.get(url, params=params, headers=API_KEY_HEADER)

#     if resp.status_code != 200:
#         raise HTTPException(status_code=resp.status_code, detail="Error fetching price")

#     data = resp.json()
#     if coin_id not in data:
#         raise HTTPException(status_code=404, detail="Coin not found")

#     return {"coin": coin_id, "currency": vs_currency, "price": data[coin_id][vs_currency]}

# app/routers/prices.py
from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.db import store
from app.schemas import PricesResponse

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/", response_model=PricesResponse)
def get_prices(ids: List[str] = Query(..., description="list of coin ids, e.g. ids=bitcoin,ethereum")):
    prices = store.get_prices(ids)
    if not prices:
        raise HTTPException(status_code=404, detail="No prices found")
    return prices
