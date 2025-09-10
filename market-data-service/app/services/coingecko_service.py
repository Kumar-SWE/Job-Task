# # app/services/coingecko_service.py
# import time
# from typing import List, Dict, Any, Optional
# import requests
# from app.config import ROOT_URL, API_KEY_HEADER

# SESSION = requests.Session()
# SESSION.headers.update({"Accept": "application/json", **API_KEY_HEADER})


# def _get(path: str, params: Optional[Dict[str, Any]] = None, timeout: int = 10) -> Dict[str, Any]:
#     url = f"{ROOT_URL.rstrip('/')}/{path.lstrip('/')}"
#     resp = SESSION.get(url, params=params, timeout=timeout)
#     resp.raise_for_status()
#     return resp.json()


# def fetch_currency_list(per_page: int = 100, page: int = 1, vs_currency: str = "inr") -> List[Dict[str, Any]]:
#     """
#     Returns list of coins with keys: id, symbol, name, logo_url, rank
#     """
#     params = {"vs_currency": vs_currency, "order": "market_cap_desc", "per_page": per_page, "page": page, "sparkline": "false"}
#     data = _get("/coins/markets", params=params)
#     out = []
#     for c in data:
#         out.append({
#             "id": c.get("id"),
#             "symbol": c.get("symbol"),
#             "name": c.get("name"),
#             "logo_url": c.get("image"),
#             "rank": c.get("market_cap_rank"),
#         })
#     return out


# def fetch_currency_detail(coin_id: str, vs_currency: str = "inr") -> Dict[str, Any]:
#     """
#     Returns a dict compatible with your CurrencyDetail schema
#     """
#     params = {"localization": "false", "tickers": "false", "market_data": "true", "community_data": "false", "developer_data": "false", "sparkline": "false"}
#     data = _get(f"/coins/{coin_id}", params=params)

#     market = data.get("market_data", {}) or {}
#     current_price = market.get("current_price", {}) or {}
#     market_cap = market.get("market_cap", {}) or {}
#     total_volume = market.get("total_volume", {}) or {}

#     return {
#         "id": data.get("id"),
#         "symbol": data.get("symbol"),
#         "name": data.get("name"),
#         "description": (data.get("description") or {}).get("en"),
#         "current_price_inr": current_price.get("inr"),
#         "market_cap_inr": market_cap.get("inr"),
#         "volume_24h_inr": total_volume.get("inr"),
#         "circulating_supply": market.get("circulating_supply"),
#         "rank": data.get("market_cap_rank"),
#     }


# def fetch_prices(coin_ids: List[str], vs_currency: str = "inr") -> Dict[str, Dict[str, float]]:
#     if not coin_ids:
#         return {}
#     ids = ",".join(coin_ids)
#     params = {"ids": ids, "vs_currencies": vs_currency}
#     data = _get("/simple/price", params=params)
#     # map to {id: {"inr": value}}
#     out = {}
#     for cid, val in data.items():
#         out[cid] = {vs_currency: val.get(vs_currency)}
#     return out


# def fetch_history(coin_id: str, days: int = 7, vs_currency: str = "inr") -> List[Dict[str, Any]]:
#     """
#     Returns an array of candles with fields matching HistoryCandle:
#     ts, open, high, low, close, volume
#     * Note: CoinGecko returns 'prices' = [ [ts, price], ... ]
#       We approximate OHLC by using the price for open/high/low/close (best-effort).
#       Volume uses total_volumes entry if present.
#     """
#     params = {"vs_currency": vs_currency, "days": days, "interval": "daily"}
#     data = _get(f"/coins/{coin_id}/market_chart", params=params)

#     prices = data.get("prices", [])  # list of [ts, price]
#     volumes = data.get("total_volumes", [])  # list of [ts, volume]
#     candles = []
#     for i, p in enumerate(prices):
#         ts, price = p[0], p[1]
#         vol = volumes[i][1] if i < len(volumes) and isinstance(volumes[i], list) else 0.0
#         candles.append({
#             "ts": str(ts),
#             "open": price,
#             "high": price,
#             "low": price,
#             "close": price,
#             "volume": vol,
#         })
#     return candles


# def fetch_global() -> Dict[str, Any]:
#     data = _get("/global")
#     return data.get("data", {})


# def fetch_trending() -> List[Dict[str, Any]]:
#     """
#     Returns list of trending items (CoinGecko /search/trending -> coins[*].item)
#     """
#     data = _get("/search/trending")
#     coins = data.get("coins", [])
#     out = []
#     for entry in coins:
#         item = entry.get("item", {})
#         out.append(item)
#     return out


# app/services/coingecko_service.py
import os
from typing import List, Dict, Any, Optional
import requests

BASE_URL = os.getenv("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3")
API_KEY = os.getenv("COINGECKO_API_KEY")

SESSION = requests.Session()
SESSION.headers.update({"Accept": "application/json"})
if API_KEY:
    SESSION.headers.update({"x-cg-demo-api-key": API_KEY})


def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    resp = SESSION.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_currency_list(per_page: int = 100, page: int = 1, vs_currency: str = "inr") -> List[Dict[str, Any]]:
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": "false"
    }
    data = _get("/coins/markets", params=params)
    return [
        {
            "id": c.get("id"),
            "symbol": c.get("symbol"),
            "name": c.get("name"),
            "logo_url": c.get("image"),
            "rank": c.get("market_cap_rank"),
        }
        for c in data
    ]


def fetch_currency_detail(coin_id: str) -> Dict[str, Any]:
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false"
    }
    data = _get(f"/coins/{coin_id}", params=params)
    market = data.get("market_data", {}) or {}
    return {
        "id": data.get("id"),
        "symbol": data.get("symbol"),
        "name": data.get("name"),
        "description": (data.get("description") or {}).get("en"),
        "current_price_inr": market.get("current_price", {}).get("inr"),
        "market_cap_inr": market.get("market_cap", {}).get("inr"),
        "volume_24h_inr": market.get("total_volume", {}).get("inr"),
        "circulating_supply": market.get("circulating_supply"),
        "rank": data.get("market_cap_rank"),
    }


def fetch_prices(coin_ids: List[str], vs_currency: str = "inr") -> Dict[str, Dict[str, float]]:
    if not coin_ids:
        return {}
    params = {"ids": ",".join(coin_ids), "vs_currencies": vs_currency}
    data = _get("/simple/price", params=params)
    return {cid: {vs_currency: val.get(vs_currency)} for cid, val in data.items()}


def fetch_history(coin_id: str, days: int = 7, vs_currency: str = "inr") -> List[Dict[str, Any]]:
    params = {"vs_currency": vs_currency, "days": days, "interval": "daily"}
    data = _get(f"/coins/{coin_id}/market_chart", params=params)
    prices = data.get("prices", [])
    volumes = data.get("total_volumes", [])
    candles = []
    for i, (ts, price) in enumerate(prices):
        vol = volumes[i][1] if i < len(volumes) and isinstance(volumes[i], list) else 0.0
        candles.append({
            "ts": str(ts),
            "open": price,
            "high": price,
            "low": price,
            "close": price,
            "volume": vol,
        })
    return candles


def fetch_global() -> Dict[str, Any]:
    return _get("/global").get("data", {})


def fetch_trending() -> List[Dict[str, Any]]:
    data = _get("/search/trending")
    return [entry.get("item", {}) for entry in data.get("coins", [])]
