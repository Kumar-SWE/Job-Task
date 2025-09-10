# from fastapi import APIRouter, Query
# from typing import List, Literal
# from app.db import store

# router = APIRouter(prefix="/movers", tags=["movers"])

# @router.get("")
# def get_movers(type: Literal["gainers", "losers"] = Query(..., description="Type of movers: gainers or losers")):
    
#     currencies = store.get_currency_list()
#     if not currencies:
#         return []
#     if type == "gainers":
#         return currencies[:2]   
#     else:
#         return currencies[-2:]  

# from fastapi import APIRouter, HTTPException
# import httpx
# from app.config import ROOT_URL, API_KEY_HEADER

# router = APIRouter(
#     prefix="/movers",
#     tags=["movers"]
# )

# @router.get("/")
# async def get_movers():
#     """
#     Get trending cryptocurrencies (top movers)
#     """
#     url = f"{ROOT_URL}/search/trending"
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(url, headers=API_KEY_HEADER)

#     if resp.status_code != 200:
#         raise HTTPException(status_code=resp.status_code, detail="Error fetching movers")

#     return resp.json()["coins"]

# app/routers/movers.py
from fastapi import APIRouter
from app.db import store

router = APIRouter(prefix="/movers", tags=["movers"])


@router.get("/")
def get_movers():
    return store.get_movers()
