# Market Data Service (FastAPI)

## Setup

```bash
cd market-data-service
python -m venv .venv
source .venv/bin/activate   
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## showing

http://127.0.0.1:8000/api/v1/currencies
http://127.0.0.1:8000/api/v1/prices?ids=bitcoin&fiat=inr
http://127.0.0.1:8000/api/v1/prices
http://127.0.0.1:8000/api/v1/currencies?per_page=50
http://127.0.0.1:8000/api/v1/currencies/bitcoin
http://127.0.0.1:8000/api/v1/global/
http://127.0.0.1:8000/api/v1/movers/?type=losers
http://127.0.0.1:8000/api/v1/movers?type=gainers
http://127.0.0.1:8000/openapi.json
http://127.0.0.1:8000/api/v1/history/bitcoin
http://127.0.0.1:8000/api/v1/history/bitcoin?days=7

## Not Working
# http://127.0.0.1:8000/api/v1/history/bitcoin
# http://127.0.0.1:8000/api/v1/global
# http://127.0.0.1:8000/openapi.json
# http://127.0.0.1:8000/api/v1/movers?type=losers
# http://127.0.0.1:8000/api/v1/movers?type=gainers