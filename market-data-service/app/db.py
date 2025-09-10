# import json
# import os
# from typing import Dict, Any, List, Optional

# DATA_FILE = os.getenv("DATA_FILE", os.path.join(os.path.dirname(__file__), "..", "data", "seed.json"))

# class DataStore:
#     def __init__(self, path: str):
#         self.path = path
#         self._raw: Dict[str, Any] = {}
#         self.currencies: List[Dict[str, Any]] = []
#         self.currency_details: Dict[str, Any] = {}
#         self.prices: Dict[str, Dict[str, float]] = {}
#         self.history: Dict[str, List[Dict[str, Any]]] = {}

#     def load(self):
#         with open(self.path, "r", encoding="utf-8") as f:
#             self._raw = json.load(f)


#         self.currencies = self._raw.get("currencies", [])

#         details = self._raw.get("currency_details")
#         if details and isinstance(details, dict) and details.get("id"):
#             self.currency_details[details["id"]] = details

       
#         raw_prices = self._raw.get("prices", {})
#         self.prices = {k: {"inr": v.get("inr")} for k, v in raw_prices.items() if isinstance(v, dict) and "inr" in v}

        
#         raw_hist = self._raw.get("history", [])
#         if raw_hist:
          
#             hid = details["id"] if details and details.get("id") else "bitcoin"
#             self.history[hid] = raw_hist

#     def get_currency_list(self) -> List[Dict[str, Any]]:
#         return self.currencies

#     def get_currency_detail(self, cid: str) -> Optional[Dict[str, Any]]:
      
#         if cid in self.currency_details:
#             return self.currency_details[cid]

       
#         base = next((c for c in self.currencies if c.get("id") == cid), None)
#         if not base:
#             return None

#         price_inr = None
    
#         if cid in self.prices and "inr" in self.prices[cid]:
#             price_inr = self.prices[cid]["inr"]

      
#         return {
#             "id": base.get("id"),
#             "symbol": base.get("symbol"),
#             "name": base.get("name"),
#             "description": None,
#             "current_price_inr": price_inr,
#             "market_cap_inr": None,
#             "volume_24h_inr": None,
#             "circulating_supply": None,
#             "rank": base.get("rank"),
#         }

#     def get_prices(self, ids: List[str]) -> Dict[str, Dict[str, float]]:
#         out = {}
#         for cid in ids:
            
#             if cid in self.prices:
#                 out[cid] = self.prices[cid]
#         return out

#     def get_history(self, cid: str) -> List[Dict[str, Any]]:
#         return self.history.get(cid, [])


# store = DataStore(DATA_FILE)
# store.load()


# app/db.py
# from typing import Dict, Any, List, Optional
# from app.services.coingecko_service import (
#     fetch_currency_list,
#     fetch_currency_detail,
#     fetch_prices,
#     fetch_history,
#     fetch_global,
#     fetch_trending
# )

# class DataStore:
#     def __init__(self):
#         self.currencies: List[Dict[str, Any]] = []
#         self.currency_details: Dict[str, Any] = {}
#         self.prices: Dict[str, Dict[str, float]] = {}
#         self.history: Dict[str, List[Dict[str, Any]]] = {}
#         self._global: Dict[str, Any] = {}
#         self._movers: List[Dict[str, Any]] = []

#     def load(self):
#         """
#         Run at startup to populate the currency list (top N by market cap).
#         """
#         try:
#             self.currencies = fetch_currency_list(per_page=100, page=1)
#         except Exception as e:
#             print(f"[DataStore] Error loading currency list: {e}")
#             self.currencies = []

#     def get_currency_list(self) -> List[Dict[str, Any]]:
#         return self.currencies

#     def get_currency_detail(self, cid: str) -> Optional[Dict[str, Any]]:
#         # Return cached detail if present
#         if cid in self.currency_details:
#             return self.currency_details[cid]
#         try:
#             detail = fetch_currency_detail(cid)
#             if detail:
#                 self.currency_details[cid] = detail
#                 return detail
#         except Exception as e:
#             print(f"[DataStore] Error fetching detail for {cid}: {e}")

#         # Fallback to basic info from currency list
#         base = next((c for c in self.currencies if c.get("id") == cid), None)
#         if not base:
#             return None

#         return {
#             "id": base.get("id"),
#             "symbol": base.get("symbol"),
#             "name": base.get("name"),
#             "description": None,
#             "current_price_inr": None,
#             "market_cap_inr": None,
#             "volume_24h_inr": None,
#             "circulating_supply": None,
#             "rank": base.get("rank"),
#         }

#     def get_prices(self, ids: List[str]) -> Dict[str, Dict[str, float]]:
#         try:
#             prices = fetch_prices(ids)
#             # update cache
#             self.prices.update(prices)
#             return prices
#         except Exception as e:
#             print(f"[DataStore] Error fetching prices: {e}")
#             # fallback to cached values if available
#             out = {}
#             for cid in ids:
#                 if cid in self.prices:
#                     out[cid] = self.prices[cid]
#             return out

#     def get_history(self, cid: str, days: int = 7) -> List[Dict[str, Any]]:
#         try:
#             hist = fetch_history(cid, days=days)
#             self.history[cid] = hist
#             return hist
#         except Exception as e:
#             print(f"[DataStore] Error fetching history for {cid}: {e}")
#             return self.history.get(cid, [])

#     def get_global_stats(self) -> Dict[str, Any]:
#         try:
#             self._global = fetch_global()
#         except Exception as e:
#             print(f"[DataStore] Error fetching global stats: {e}")
#         return self._global

#     def get_movers(self) -> List[Dict[str, Any]]:
#         try:
#             self._movers = fetch_trending()
#         except Exception as e:
#             print(f"[DataStore] Error fetching movers: {e}")
#         return self._movers


# # singleton store used by routers
# store = DataStore()
# store.load()


import asyncio
from typing import Dict, Any, List, Optional
from app.services.coingecko_service import (
    fetch_currency_list,
    fetch_currency_detail,
    fetch_prices,
    fetch_history,
    fetch_global,
    fetch_trending
)

class DataStore:
    def __init__(self):
        self.currencies: List[Dict[str, Any]] = []
        self.currency_details: Dict[str, Any] = {}
        self.prices: Dict[str, Dict[str, float]] = {}
        self.history: Dict[str, List[Dict[str, Any]]] = {}
        self._global: Dict[str, Any] = {}
        self._movers: List[Dict[str, Any]] = []

    async def refresh_currencies_loop(self, interval_seconds: int = 180):
        """Background loop to refresh currencies every `interval_seconds`."""
        while True:
            try:
                self.currencies = fetch_currency_list(per_page=100, page=1)
                print("[DataStore] Currency list refreshed")
            except Exception as e:
                print(f"[DataStore] Error refreshing currency list: {e}")
            await asyncio.sleep(interval_seconds)

    def load(self):
        """Initial synchronous load (startup)."""
        try:
            self.currencies = fetch_currency_list(per_page=100, page=1)
            print("[DataStore] Initial currency list loaded")
        except Exception as e:
            print(f"[DataStore] Error loading currency list: {e}")
            self.currencies = []

    def get_currency_list(self) -> List[Dict[str, Any]]:
        return self.currencies

    def get_currency_detail(self, cid: str) -> Optional[Dict[str, Any]]:
        # Return cached detail if present
        if cid in self.currency_details:
            return self.currency_details[cid]
        try:
            detail = fetch_currency_detail(cid)
            if detail:
                self.currency_details[cid] = detail
                return detail
        except Exception as e:
            print(f"[DataStore] Error fetching detail for {cid}: {e}")

        # Fallback to basic info from currency list
        base = next((c for c in self.currencies if c.get("id") == cid), None)
        if not base:
            return None

        return {
            "id": base.get("id"),
            "symbol": base.get("symbol"),
            "name": base.get("name"),
            "description": None,
            "current_price_inr": None,
            "market_cap_inr": None,
            "volume_24h_inr": None,
            "circulating_supply": None,
            "rank": base.get("rank"),
        }

    def get_prices(self, ids: List[str]) -> Dict[str, Dict[str, float]]:
        try:
            prices = fetch_prices(ids)
            # update cache
            self.prices.update(prices)
            return prices
        except Exception as e:
            print(f"[DataStore] Error fetching prices: {e}")
            # fallback to cached values if available
            out = {}
            for cid in ids:
                if cid in self.prices:
                    out[cid] = self.prices[cid]
            return out

    def get_history(self, cid: str, days: int = 7) -> List[Dict[str, Any]]:
        try:
            hist = fetch_history(cid, days=days)
            self.history[cid] = hist
            return hist
        except Exception as e:
            print(f"[DataStore] Error fetching history for {cid}: {e}")
            return self.history.get(cid, [])

    def get_global_stats(self) -> Dict[str, Any]:
        try:
            self._global = fetch_global()
        except Exception as e:
            print(f"[DataStore] Error fetching global stats: {e}")
        return self._global

    def get_movers(self) -> List[Dict[str, Any]]:
        try:
            self._movers = fetch_trending()
        except Exception as e:
            print(f"[DataStore] Error fetching movers: {e}")
        return self._movers


# singleton store used by routers
store = DataStore()
store.load()
