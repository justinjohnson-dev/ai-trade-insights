import os

from fastapi import APIRouter, HTTPException
from polygon import RESTClient
from dotenv import load_dotenv
from app.controllers.playground import (
    fetch_two_years_historical_data,
    calculate_technical_indicators,
)
from app.utils.app_logger import log_exception

playground_router = APIRouter(
    prefix="/v1/api",
    tags=["playground"],
)

load_dotenv()

API_KEY = os.getenv("POLYGON_API_KEY")


@playground_router.get("/playground")
async def playground():
    try:
        client = RESTClient(API_KEY)
        aggs = fetch_two_years_historical_data(client, ticker="SPY")
        return {
            "sma": f"${round(calculate_technical_indicators(aggs), 2)}",
            "ticker": "SPY",
            "period": 45,
            "aggs": aggs,
        }
    except Exception as e:
        log_exception()
        raise HTTPException(status_code=500, detail=str(e)) from e
