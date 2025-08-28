from typing import List, Dict, Optional
from pydantic import BaseModel, Field, RootModel


class Currency(BaseModel):
    id: str
    symbol: str
    name: str
    logo_url: Optional[str] = None
    rank: Optional[int] = None


class CurrencyDetail(BaseModel):
    id: str
    symbol: str
    name: str
    description: Optional[str] = None
    current_price_inr: Optional[float] = None
    market_cap_inr: Optional[float] = None
    volume_24h_inr: Optional[float] = None
    circulating_supply: Optional[float] = None
    rank: Optional[int] = None


class PriceEntry(BaseModel):
    inr: float

class PricesResponse(RootModel[Dict[str, PriceEntry]]):
    pass


class HistoryCandle(BaseModel):
    ts: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class APIMessage(BaseModel):
    message: str = Field(default="ok")
