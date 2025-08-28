import json
import os
from typing import Dict, Any, List, Optional

DATA_FILE = os.getenv("DATA_FILE", os.path.join(os.path.dirname(__file__), "..", "data", "seed.json"))

class DataStore:
    def __init__(self, path: str):
        self.path = path
        self._raw: Dict[str, Any] = {}
        self.currencies: List[Dict[str, Any]] = []
        self.currency_details: Dict[str, Any] = {}
        self.prices: Dict[str, Dict[str, float]] = {}
        self.history: Dict[str, List[Dict[str, Any]]] = {}

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self._raw = json.load(f)


        self.currencies = self._raw.get("currencies", [])

        details = self._raw.get("currency_details")
        if details and isinstance(details, dict) and details.get("id"):
            self.currency_details[details["id"]] = details

       
        raw_prices = self._raw.get("prices", {})
        self.prices = {k: {"inr": v.get("inr")} for k, v in raw_prices.items() if isinstance(v, dict) and "inr" in v}

        
        raw_hist = self._raw.get("history", [])
        if raw_hist:
          
            hid = details["id"] if details and details.get("id") else "bitcoin"
            self.history[hid] = raw_hist

    def get_currency_list(self) -> List[Dict[str, Any]]:
        return self.currencies

    def get_currency_detail(self, cid: str) -> Optional[Dict[str, Any]]:
      
        if cid in self.currency_details:
            return self.currency_details[cid]

       
        base = next((c for c in self.currencies if c.get("id") == cid), None)
        if not base:
            return None

        price_inr = None
    
        if cid in self.prices and "inr" in self.prices[cid]:
            price_inr = self.prices[cid]["inr"]

      
        return {
            "id": base.get("id"),
            "symbol": base.get("symbol"),
            "name": base.get("name"),
            "description": None,
            "current_price_inr": price_inr,
            "market_cap_inr": None,
            "volume_24h_inr": None,
            "circulating_supply": None,
            "rank": base.get("rank"),
        }

    def get_prices(self, ids: List[str]) -> Dict[str, Dict[str, float]]:
        out = {}
        for cid in ids:
            
            if cid in self.prices:
                out[cid] = self.prices[cid]
        return out

    def get_history(self, cid: str) -> List[Dict[str, Any]]:
        return self.history.get(cid, [])


store = DataStore(DATA_FILE)
store.load()
