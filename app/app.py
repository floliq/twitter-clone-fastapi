from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.responses import FileResponse, PlainTextResponse
from starlette.staticfiles import StaticFiles

from app.db import init_db, create_first_user
from app.routing import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is running")
    await init_db()
    await create_first_user()
    yield
    print("Server is shutting dow")


def create_app():
    app = FastAPI(
        title="Twitter clone",
        version="1.0.0",
        description="Twitter clone realized by FastAPI framework",
        lifespan=lifespan,
    )

    dist_path = Path("app/dist")

    app.mount("/css", StaticFiles(directory=dist_path / "css"), name="css")
    app.mount("/js", StaticFiles(directory=dist_path / "js"), name="js")
    app.mount("/media", StaticFiles(directory=dist_path), name="media")
    app.include_router(router)

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
