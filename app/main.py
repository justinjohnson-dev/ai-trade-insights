from fastapi import FastAPI

from app.routers.app_router import app_router
from app.routers.playground import playground_router


from app.utils.app_logger import app_logger

app = FastAPI()


@app.get("/")
async def root():
    app_logger.info("AI Trade Insights")
    return {"message": "AI Trade Insights"}


app.include_router(app_router)
app.include_router(playground_router)
