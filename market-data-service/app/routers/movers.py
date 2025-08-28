from fastapi import APIRouter, Query
from typing import List, Literal
from app.db import store

router = APIRouter(prefix="/movers", tags=["movers"])

@router.get("")
def get_movers(type: Literal["gainers", "losers"] = Query(..., description="Type of movers: gainers or losers")):
    
    currencies = store.get_currency_list()
    if not currencies:
        return []
    if type == "gainers":
        return currencies[:2]   
    else:
        return currencies[-2:]  