# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routers import currencies, prices, history, movers, global_stats
# from app.schemas import APIMessage

# app = FastAPI(
#     title="Market Data Service",
#     version="1.0.0",
#     docs_url="/docs",
#     openapi_url="/openapi.json"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/", response_model=APIMessage)
# def root():
#     return {"message": "market-data-service ok"}

# app.include_router(currencies.router, prefix="/api/v1")
# app.include_router(prices.router, prefix="/api/v1")
# app.include_router(history.router, prefix="/api/v1")
# app.include_router(movers.router, prefix="/api/v1")
# app.include_router(global_stats.router, prefix="/api/v1")

# from fastapi import FastAPI
# from app.routers import currencies, global_stats, history, movers, prices

# app = FastAPI(title="Crypto Market API Service")

# # Include routers
# app.include_router(currencies.router)
# app.include_router(global_stats.router)
# app.include_router(history.router)
# app.include_router(movers.router)
# app.include_router(prices.router)

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Crypto Market API Service!"}

# app/main.py
# from fastapi import FastAPI
# from app.routers import currencies, global_stats, history, movers, prices

# app = FastAPI(title="Market Data Service", version="1.0.0")

# # Include routers (each router file defines its own /prefix)
# app.include_router(currencies.router, prefix="/api/v1")
# app.include_router(global_stats.router, prefix="/api/v1")
# app.include_router(history.router, prefix="/api/v1")
# app.include_router(movers.router, prefix="/api/v1")
# app.include_router(prices.router, prefix="/api/v1")


# @app.get("/")
# async def root():
#     return {"message": "Market Data Service running"}

# from fastapi import FastAPI
# from app.routers import currencies, global_stats, history, movers, prices
# from app.db import store
# import asyncio

# app = FastAPI(title="Market Data Service", version="1.0.0")

# # Include routers
# app.include_router(currencies.router, prefix="/api/v1")
# app.include_router(global_stats.router, prefix="/api/v1")
# app.include_router(history.router, prefix="/api/v1")
# app.include_router(movers.router, prefix="/api/v1")
# app.include_router(prices.router, prefix="/api/v1")


# @app.get("/")
# async def root():
#     return {"message": "Market Data Service running"}


# @app.on_event("startup")
# async def startup_event():
#     """
#     On startup, start background tasks:
#     - Refresh currency list every 3 minutes
#     """
#     asyncio.create_task(store.refresh_loop(interval_seconds=100))


from fastapi import FastAPI, HTTPException
from app.db import store
import asyncio
import mysql.connector

app = FastAPI(title="Market Data Service", version="1.0.0")

# MySQL connection (read-only for endpoints)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # change if needed
        password="1234",  # replace with your MySQL root password
        database="crypto_data"
    )


@app.get("/")
async def root():
    return {"message": "Market Data Service running"}


@app.get("/api/v1/currencies")
async def get_currencies():
    """Return all currencies from MySQL"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM currencies ORDER BY `rank` ASC LIMIT 50")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


@app.get("/api/v1/currencies/{currency_id}")
async def get_currency(currency_id: str):
    """Return details for a single currency"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM currencies WHERE id = %s", (currency_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Currency not found")
    return result


@app.get("/api/v1/prices")
async def get_prices(ids: str):
    """
    Get current prices for a comma-separated list of currency IDs.
    Example: /api/v1/prices?ids=bitcoin,ethereum
    """
    id_list = ids.split(",")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    format_strings = ",".join(["%s"] * len(id_list))
    cursor.execute(
        f"SELECT id, current_price_inr, market_cap_inr, volume_24h_inr FROM currencies WHERE id IN ({format_strings})",
        tuple(id_list),
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row["id"]: {
        "current_price_inr": row["current_price_inr"],
        "market_cap_inr": row["market_cap_inr"],
        "volume_24h_inr": row["volume_24h_inr"]
    } for row in result}


@app.on_event("startup")
async def startup_event():
    """
    Start background task: refresh markets every 100 seconds
    """
    asyncio.create_task(store.refresh_loop(interval_seconds=100))
