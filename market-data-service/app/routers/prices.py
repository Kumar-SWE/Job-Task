from fastapi import APIRouter, Query
from typing import List
from app.schemas import PricesResponse
from app.db import store

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=PricesResponse)
def get_prices(
    ids: List[str] = Query(..., description="Comma-separated currency ids e.g. ids=bitcoin,ethereum"),
    fiat: str = Query("inr"),
):
    if fiat.lower() != "inr":
        
        return {}

   
    normalized_ids: List[str] = []
    for part in ids:
        normalized_ids.extend([x.strip() for x in part.split(",") if x.strip()])

    data = store.get_prices(normalized_ids)

    return data 

