import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.responses import FileResponse, PlainTextResponse
from starlette.staticfiles import StaticFiles

from app.db import create_first_user
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
    )
    dist_path = app_path / "dist"

    css_path = dist_path / "css"
    js_path = dist_path / "js"
    media_path = app_path / "media"

    if css_path.exists():
        app.mount("/css", StaticFiles(directory=css_path), name="css")

    if js_path.exists():
        app.mount("/js", StaticFiles(directory=js_path), name="js")

    if dist_path.exists():
        app.mount("/media", StaticFiles(directory=media_path), name="media")

    app.include_router(user_router)
    app.include_router(tweet_router)
    app.include_router(media_router)

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return FileResponse(dist_path / "favicon.ico")

    # корневой index.html
    @app.get("/", include_in_schema=False)
    async def index():
        return FileResponse(dist_path / "index.html")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str):
        if full_path.startswith(("api", "media", "css", "js", "favicon.ico")):
            return PlainTextResponse("Not Found", status_code=404)
        return FileResponse(dist_path / "index.html")

    return app
