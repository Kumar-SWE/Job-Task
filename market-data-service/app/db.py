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


# import asyncio
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

#     async def refresh_currencies_loop(self, interval_seconds: int = 10):
#         """Background loop to refresh currencies every `interval_seconds`."""
#         while True:
#             try:
#                 self.currencies = fetch_currency_list(per_page=100, page=1)
#                 print("[DataStore] Currency list refreshed")
#             except Exception as e:
#                 print(f"[DataStore] Error refreshing currency list: {e}")
#             await asyncio.sleep(interval_seconds)

#     def load(self):
#         """Initial synchronous load (startup)."""
#         try:
#             self.currencies = fetch_currency_list(per_page=100, page=1)
#             print("[DataStore] Initial currency list loaded")
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


# import asyncio
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

#     async def refresh_currencies_loop(self, interval_seconds: int = 180):
#         """Background loop to refresh currencies every `interval_seconds`."""
#         while True:
#             try:
#                 # Run synchronous fetch in a separate thread to avoid blocking
#                 self.currencies = await asyncio.to_thread(fetch_currency_list, per_page=100, page=1)
#                 print("[DataStore] Currency list refreshed")
#             except Exception as e:
#                 print(f"[DataStore] Error refreshing currency list: {e}")
#             await asyncio.sleep(interval_seconds)

#     def load(self):
#         """Initial synchronous load (startup)."""
#         try:
#             self.currencies = fetch_currency_list(per_page=100, page=1)
#             print("[DataStore] Initial currency list loaded")
#         except Exception as e:
#             print(f"[DataStore] Error loading currency list: {e}")
#             self.currencies = []

#     def get_currency_list(self) -> List[Dict[str, Any]]:
#         return self.currencies

#     def get_currency_detail(self, cid: str) -> Optional[Dict[str, Any]]:
#         if cid in self.currency_details:
#             return self.currency_details[cid]
#         try:
#             detail = fetch_currency_detail(cid)
#             if detail:
#                 self.currency_details[cid] = detail
#                 return detail
#         except Exception as e:
#             print(f"[DataStore] Error fetching detail for {cid}: {e}")

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
#             self.prices.update(prices)
#             return prices
#         except Exception as e:
#             print(f"[DataStore] Error fetching prices: {e}")
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


# # Singleton store used by routers
# store = DataStore()
# store.load()

# import asyncio
# from typing import Dict, Any, List, Optional
# import datetime
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

#     async def refresh_loop(self, interval_seconds: int = 100):
#         """Background loop to refresh all data every `interval_seconds`."""
#         while True:
#             try:
#                 # Refresh currency list
#                 self.currencies = await asyncio.to_thread(fetch_currency_list, per_page=100, page=1)
#                 print(f"[DataStore] Currency list refreshed at {datetime.datetime.now()}")

#                 # Refresh prices for all currencies
#                 ids = [c.get("id") for c in self.currencies]
#                 if ids:
#                     self.prices = await asyncio.to_thread(fetch_prices, ids)
#                     print(f"[DataStore] Prices refreshed at {datetime.datetime.now()}")

#                 # Refresh global stats
#                 self._global = await asyncio.to_thread(fetch_global)
#                 print(f"[DataStore] Global stats refreshed at {datetime.datetime.now()}")

#                 # Refresh trending movers
#                 self._movers = await asyncio.to_thread(fetch_trending)
#                 print(f"[DataStore] Trending movers refreshed at {datetime.datetime.now()}")

#             except Exception as e:
#                 print(f"[DataStore] Error in background refresh: {e}")

#             await asyncio.sleep(interval_seconds)

#     def load(self):
#         """Initial synchronous load at startup."""
#         try:
#             self.currencies = fetch_currency_list(per_page=100, page=1)
#             print(f"[DataStore] Initial currency list loaded at {datetime.datetime.now()}")
#         except Exception as e:
#             print(f"[DataStore] Error loading currency list: {e}")
#             self.currencies = []

#     def get_currency_list(self) -> List[Dict[str, Any]]:
#         return self.currencies

#     def get_currency_detail(self, cid: str) -> Optional[Dict[str, Any]]:
#         if cid in self.currency_details:
#             return self.currency_details[cid]
#         try:
#             detail = fetch_currency_detail(cid)
#             if detail:
#                 self.currency_details[cid] = detail
#                 return detail
#         except Exception as e:
#             print(f"[DataStore] Error fetching detail for {cid}: {e}")

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
#             self.prices.update(prices)
#             return prices
#         except Exception as e:
#             print(f"[DataStore] Error fetching prices: {e}")
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
#         return self._global

#     def get_movers(self) -> List[Dict[str, Any]]:
#         return self._movers


# # Singleton store used by routers
# store = DataStore()
# store.load()

import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
import mysql.connector
from mysql.connector import Error

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
        # In-memory cache
        self.currencies: List[Dict[str, Any]] = []
        self.currency_details: Dict[str, Any] = {}
        self.prices: Dict[str, Dict[str, float]] = {}
        self.history: Dict[str, List[Dict[str, Any]]] = {}
        self._global: Dict[str, Any] = {}
        self._movers: List[Dict[str, Any]] = {}

        # MySQL connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",      # change if not local
                user="root",           # your MySQL username
                password="1234",  # your MySQL password
                database="crypto_data"
            )
            self.cursor = self.conn.cursor()
            print("[MySQL] Connected successfully.")
        except Error as e:
            print(f"[MySQL] Connection error: {e}")
            self.conn = None
            self.cursor = None

    # 🔄 save currencies into MySQL
    def save_currencies_to_db(self, currencies: List[Dict[str, Any]]):
        if not self.conn or not self.cursor:
            print("[MySQL] Skipped saving, no DB connection.")
            return

        try:
            for c in currencies:
                query = """
                INSERT INTO currencies (id, symbol, name, logo_url, `rank`, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    symbol = VALUES(symbol),
                    name = VALUES(name),
                    logo_url = VALUES(logo_url),
                    `rank` = VALUES(`rank`),
                    last_updated = VALUES(last_updated);
                """
                values = (
                    c.get("id"),
                    c.get("symbol"),
                    c.get("name"),
                    c.get("logo_url"),
                    c.get("rank"),
                    datetime.now()
                )
                self.cursor.execute(query, values)
            self.conn.commit()
            print(f"[MySQL] Saved {len(currencies)} currencies at {datetime.now()}")
        except Error as e:
            print(f"[MySQL] Error saving currencies: {e}")

    def save_prices_to_db(self, prices: Dict[str, Dict[str, Any]]):
        if not self.conn or not self.cursor:
            return

        try:
            for cid, pdata in prices.items():
                query = """
                UPDATE currencies
                SET current_price_inr = %s,
                    market_cap_inr = %s,
                    volume_24h_inr = %s,
                    last_updated = %s
                WHERE id = %s;
                """
                values = (
                    pdata.get("inr"),                  # current price
                    pdata.get("inr_market_cap"),       # market cap
                    pdata.get("inr_24h_vol"),          # 24h volume
                    datetime.now(),
                    cid
                )
                self.cursor.execute(query, values)
            self.conn.commit()
            print(f"[MySQL] Updated prices for {len(prices)} currencies at {datetime.now()}")
        except Error as e:
            print(f"[MySQL] Error saving prices: {e}")

    

    async def refresh_loop(self, interval_seconds: int = 100):
        """Background loop to refresh data every N seconds."""
        while True:
            try:
                # currencies
                self.currencies = fetch_currency_list(per_page=100, page=1)
                print(f"[DataStore] Currency list refreshed at {datetime.now()}")
                self.save_currencies_to_db(self.currencies)

                # prices
                ids = [c["id"] for c in self.currencies]
                if ids:
                    self.prices = fetch_prices(ids)
                    print(f"[DataStore] Prices refreshed at {datetime.now()}")
                    self.save_prices_to_db(self.prices)

                # global
                self._global = fetch_global()
                print(f"[DataStore] Global stats refreshed at {datetime.now()}")

                # trending movers
                self._movers = fetch_trending()
                print(f"[DataStore] Trending movers refreshed at {datetime.now()}")

            except Exception as e:
                print(f"[DataStore] Error in refresh loop: {e}")

            await asyncio.sleep(interval_seconds)

    def load(self):
        """Initial synchronous load (startup)."""
        try:
            self.currencies = fetch_currency_list(per_page=100, page=1)
            print(f"[DataStore] Initial currency list loaded at {datetime.now()}")
            self.save_currencies_to_db(self.currencies)
        except Exception as e:
            print(f"[DataStore] Error loading currency list: {e}")
            self.currencies = []

    def get_currency_list(self) -> List[Dict[str, Any]]:
        return self.currencies

    def get_currency_detail(self, cid: str) -> Optional[Dict[str, Any]]:
        if cid in self.currency_details:
            return self.currency_details[cid]
        try:
            detail = fetch_currency_detail(cid)
            if detail:
                self.currency_details[cid] = detail
                return detail
        except Exception as e:
            print(f"[DataStore] Error fetching detail for {cid}: {e}")

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
            self.prices.update(prices)
            return prices
        except Exception as e:
            print(f"[DataStore] Error fetching prices: {e}")
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
        return self._global

    def get_movers(self) -> List[Dict[str, Any]]:
        return self._movers


# singleton store
store = DataStore()
store.load()


# import asyncio
# import aiohttp
# import mysql.connector
# from datetime import datetime


# class DataStore:
#     def __init__(self):
#         # In-memory cache
#         self.currencies = {}

#         # MySQL connection
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="root",         # change if you use another user
#             password="yourpassword",  # replace with your MySQL root password
#             database="crypto_data"
#         )
#         self.cursor = self.conn.cursor()

#         # Make sure table exists
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS currencies (
#                 id VARCHAR(50) PRIMARY KEY,
#                 symbol VARCHAR(20),
#                 name VARCHAR(100),
#                 logo_url VARCHAR(255),
#                 rank INT,
#                 current_price_inr DOUBLE,
#                 market_cap_inr DOUBLE,
#                 volume_24h_inr DOUBLE,
#                 circulating_supply DOUBLE,
#                 last_updated DATETIME
#             )
#         """)
#         self.conn.commit()

#     async def fetch_markets(self):
#         """Fetch market data (price, market cap, volume, etc.) from CoinGecko"""
#         url = (
#             "https://api.coingecko.com/api/v3/coins/markets"
#             "?vs_currency=inr&order=market_cap_desc&per_page=50&page=1&sparkline=false"
#         )

#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as resp:
#                 if resp.status == 200:
#                     data = await resp.json()
#                     self._update_currencies(data)
#                 else:
#                     print(f"[DataStore] Failed to fetch markets: {resp.status}")

#     def _update_currencies(self, data):
#         now = datetime.now()

#         for coin in data:
#             cid = coin.get("id")
#             self.currencies[cid] = {
#                 "symbol": coin.get("symbol"),
#                 "name": coin.get("name"),
#                 "logo_url": coin.get("image"),
#                 "rank": coin.get("market_cap_rank"),
#                 "current_price_inr": coin.get("current_price"),
#                 "market_cap_inr": coin.get("market_cap"),
#                 "volume_24h_inr": coin.get("total_volume"),
#                 "circulating_supply": coin.get("circulating_supply"),
#                 "last_updated": now,
#             }

#             # Upsert into MySQL
#             self.cursor.execute("""
#                 INSERT INTO currencies (id, symbol, name, logo_url, rank, current_price_inr, 
#                                         market_cap_inr, volume_24h_inr, circulating_supply, last_updated)
#                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                 ON DUPLICATE KEY UPDATE
#                     symbol=VALUES(symbol),
#                     name=VALUES(name),
#                     logo_url=VALUES(logo_url),
#                     rank=VALUES(rank),
#                     current_price_inr=VALUES(current_price_inr),
#                     market_cap_inr=VALUES(market_cap_inr),
#                     volume_24h_inr=VALUES(volume_24h_inr),
#                     circulating_supply=VALUES(circulating_supply),
#                     last_updated=VALUES(last_updated)
#             """, (
#                 cid,
#                 coin.get("symbol"),
#                 coin.get("name"),
#                 coin.get("image"),
#                 coin.get("market_cap_rank"),
#                 coin.get("current_price"),
#                 coin.get("market_cap"),
#                 coin.get("total_volume"),
#                 coin.get("circulating_supply"),
#                 now
#             ))

#         self.conn.commit()
#         print(f"[DataStore] Markets refreshed at {now}")

#     async def refresh_loop(self, interval_seconds: int = 100):
#         """Auto-refresh markets every X seconds"""
#         while True:
#             try:
#                 await self.fetch_markets()
#             except Exception as e:
#                 print(f"[DataStore] Error refreshing markets: {e}")
#             await asyncio.sleep(interval_seconds)


# # Create global store instance
# store = DataStore()

# import requests
# import mysql.connector
# from datetime import datetime


# class DataStore:
#     def __init__(self):
#         # In-memory cache
#         self.currencies = {}

#         # MySQL connection
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="root",         # change if you use another user
#             password="1234",  # replace with your MySQL root password
#             database="crypto_data"
#         )
#         self.cursor = self.conn.cursor()

#         # Make sure table exists
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS currencies (
#                 id VARCHAR(50) PRIMARY KEY,
#                 symbol VARCHAR(20),
#                 name VARCHAR(100),
#                 logo_url VARCHAR(255),
#                 rank INT,
#                 current_price_inr DOUBLE,
#                 market_cap_inr DOUBLE,
#                 volume_24h_inr DOUBLE,
#                 circulating_supply DOUBLE,
#                 last_updated DATETIME
#             )
#         """)
#         self.conn.commit()

#     def fetch_markets(self):
#         """Fetch market data (price, market cap, volume, etc.) from CoinGecko"""
#         url = (
#             "https://api.coingecko.com/api/v3/coins/markets"
#             "?vs_currency=inr&order=market_cap_desc&per_page=50&page=1&sparkline=false"
#         )

#         try:
#             resp = requests.get(url, timeout=10)
#             resp.raise_for_status()
#             data = resp.json()
#             self._update_currencies(data)
#         except Exception as e:
#             print(f"[DataStore] Error fetching markets: {e}")

#     def _update_currencies(self, data):
#         now = datetime.now()

#         for coin in data:
#             cid = coin.get("id")
#             self.currencies[cid] = {
#                 "symbol": coin.get("symbol"),
#                 "name": coin.get("name"),
#                 "logo_url": coin.get("image"),
#                 "rank": coin.get("market_cap_rank"),
#                 "current_price_inr": coin.get("current_price"),
#                 "market_cap_inr": coin.get("market_cap"),
#                 "volume_24h_inr": coin.get("total_volume"),
#                 "circulating_supply": coin.get("circulating_supply"),
#                 "last_updated": now,
#             }

#             # Upsert into MySQL
#             self.cursor.execute("""
#                 INSERT INTO currencies (id, symbol, name, logo_url, rank, current_price_inr, 
#                                         market_cap_inr, volume_24h_inr, circulating_supply, last_updated)
#                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                 ON DUPLICATE KEY UPDATE
#                     symbol=VALUES(symbol),
#                     name=VALUES(name),
#                     logo_url=VALUES(logo_url),
#                     rank=VALUES(rank),
#                     current_price_inr=VALUES(current_price_inr),
#                     market_cap_inr=VALUES(market_cap_inr),
#                     volume_24h_inr=VALUES(volume_24h_inr),
#                     circulating_supply=VALUES(circulating_supply),
#                     last_updated=VALUES(last_updated)
#             """, (
#                 cid,
#                 coin.get("symbol"),
#                 coin.get("name"),
#                 coin.get("image"),
#                 coin.get("market_cap_rank"),
#                 coin.get("current_price"),
#                 coin.get("market_cap"),
#                 coin.get("total_volume"),
#                 coin.get("circulating_supply"),
#                 now
#             ))

#         self.conn.commit()
#         print(f"[DataStore] Markets refreshed at {now}")

#     def refresh_loop(self, interval_seconds: int = 100):
#         """Auto-refresh markets every X seconds (blocking loop)"""
#         import time
#         while True:
#             try:
#                 self.fetch_markets()
#             except Exception as e:
#                 print(f"[DataStore] Error refreshing markets: {e}")
#             time.sleep(interval_seconds)


# # Create global store instance
# store = DataStore()


# import requests
# import mysql.connector
# from datetime import datetime

# class DataStore:
#     def __init__(self):
#         # In-memory cache
#         self.currencies = {}

#         # MySQL connection
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="root",         # change if needed
#             password="1234",  # replace with your MySQL root password
#             database="crypto_data"
#         )
#         self.cursor = self.conn.cursor()

#         # Make sure table exists
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS currencies (
#                 id VARCHAR(50) PRIMARY KEY,
#                 symbol VARCHAR(20),
#                 name VARCHAR(100),
#                 logo_url VARCHAR(255),
#                 rank INT,
#                 current_price_inr DOUBLE,
#                 market_cap_inr DOUBLE,
#                 volume_24h_inr DOUBLE,
#                 circulating_supply DOUBLE,
#                 last_updated DATETIME
#             )
#         """)
#         self.conn.commit()

#     def fetch_markets(self):
#         """Fetch market data (price, market cap, volume, etc.) from CoinGecko"""
#         url = (
#             "https://api.coingecko.com/api/v3/coins/markets"
#             "?vs_currency=inr&order=market_cap_desc&per_page=50&page=1&sparkline=false"
#         )

#         resp = requests.get(url, timeout=10)
#         if resp.status_code == 200:
#             data = resp.json()
#             self._update_currencies(data)
#         else:
#             print(f"[DataStore] Failed to fetch markets: {resp.status_code}")

#     def _update_currencies(self, data):
#         now = datetime.now()

#         for coin in data:
#             cid = coin.get("id")
#             self.currencies[cid] = {
#                 "symbol": coin.get("symbol"),
#                 "name": coin.get("name"),
#                 "logo_url": coin.get("image"),
#                 "rank": coin.get("market_cap_rank"),
#                 "current_price_inr": coin.get("current_price"),
#                 "market_cap_inr": coin.get("market_cap"),
#                 "volume_24h_inr": coin.get("total_volume"),
#                 "circulating_supply": coin.get("circulating_supply"),
#                 "last_updated": now,
#             }

#             # Upsert into MySQL
#             self.cursor.execute("""
#                 INSERT INTO currencies (id, symbol, name, logo_url, rank, current_price_inr, 
#                                         market_cap_inr, volume_24h_inr, circulating_supply, last_updated)
#                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                 ON DUPLICATE KEY UPDATE
#                     symbol=VALUES(symbol),
#                     name=VALUES(name),
#                     logo_url=VALUES(logo_url),
#                     rank=VALUES(rank),
#                     current_price_inr=VALUES(current_price_inr),
#                     market_cap_inr=VALUES(market_cap_inr),
#                     volume_24h_inr=VALUES(volume_24h_inr),
#                     circulating_supply=VALUES(circulating_supply),
#                     last_updated=VALUES(last_updated)
#             """, (
#                 cid,
#                 coin.get("symbol"),
#                 coin.get("name"),
#                 coin.get("image"),
#                 coin.get("market_cap_rank"),
#                 coin.get("current_price"),
#                 coin.get("market_cap"),
#                 coin.get("total_volume"),
#                 coin.get("circulating_supply"),
#                 now
#             ))

#         self.conn.commit()
#         print(f"[DataStore] Markets refreshed at {now}")


# # Create global store instance
# store = DataStore()

# if __name__ == "__main__":
#     store.fetch_markets()
