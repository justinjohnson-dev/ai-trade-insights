from fastapi import APIRouter

from app.constants.string_constants import StringConstants
from app.utils.app_logger import app_logger

app_router = APIRouter()


# fly.io health check - pings every other second
@app_router.get("/health")
async def ping():
    app_logger.info("Health check pinged")
    return {"message": StringConstants.get_health_check_msg()}
