from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import currencies, prices, history, movers, global_stats
from app.schemas import APIMessage

app = FastAPI(
    title="Market Data Service",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=APIMessage)
def root():
    return {"message": "market-data-service ok"}

app.include_router(currencies.router, prefix="/api/v1")
app.include_router(prices.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
app.include_router(movers.router, prefix="/api/v1")
app.include_router(global_stats.router, prefix="/api/v1")
