# Market Data Service (FastAPI)

## Setup

```bash
cd market-data-service
python -m venv .venv
source .venv/bin/activate   
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
