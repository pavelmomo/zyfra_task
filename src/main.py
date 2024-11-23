from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.auth_router import auth_router
from common.settings import settings
from services.sessions_service import session_service


@asynccontextmanager
async def lifespan(application: FastAPI):
    session_service.init_storage()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME, lifespan=lifespan, root_path=settings.ROOT_PATH
)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT)