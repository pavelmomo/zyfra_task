from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from common.settings import settings
from services.sessions_service import init_storage
from api.sessions_router import sessions_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    # init_storage()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(sessions_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT)
