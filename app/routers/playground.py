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


@playground_router.post("/playground")
async def playground(request: dict):
    try:
        # ticker is passed in the request body
        client = RESTClient(API_KEY)
        data = fetch_two_years_historical_data(client, ticker=request["ticker"].upper())
        return data
    except Exception as e:
        log_exception()
        raise HTTPException(status_code=500, detail=str(e)) from e
