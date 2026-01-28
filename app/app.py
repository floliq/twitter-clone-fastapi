import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI

from app.db import create_first_user
from app.exception_handlers import CustomHTTPException, custom_http_exception_handler, global_exception_handler
from app.routes.media import media_router
from app.routes.tweet import tweet_router
from app.routes.user import user_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app_path = Path("app")
static_router = APIRouter(include_in_schema=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server is running")
    await create_first_user()
    yield
    logger.info("Server is shutting dow")


def create_app():
    app = FastAPI(
        title="Twitter clone",
        version="1.0.0",
        description="Twitter clone realized by FastAPI framework",
        lifespan=lifespan,
        openapi_url="/api/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(user_router, tags=["User"])
    app.include_router(tweet_router, tags=["Tweet"])
    app.include_router(media_router, tags=["Media"])
    app.include_router(static_router)

    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    return app
