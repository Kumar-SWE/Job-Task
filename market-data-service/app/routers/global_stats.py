from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/global", tags=["global"])

@router.get("")
def get_global_stats():
    return {
        "id": "global_1",
        "total_market_cap_inr": 200_000_000_000_000,  
        "total_volume_inr": 5_000_000_000_000,        
        "btc_dominance_pct": 48.2,                    
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
