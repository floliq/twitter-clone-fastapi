from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.app import create_app
from app.db import get_session

from app.models import metadata

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


app = create_app()
app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def auth_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers={"api-key": "test"}) as client:
        yield client


@pytest.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session
