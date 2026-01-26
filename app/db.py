import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import select

from app.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)

engine = create_async_engine(url=settings.database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_first_user():
    async with async_session() as session:
        users_result = await session.execute(select(User))
        users = users_result.all()

        if users:
            logger.info(f"Database already has {len(users)} user(s)")
        else:
            first_user = User(
                username="test_user",
                api_key="test",
            )
            session.add(first_user)
            await session.commit()
            logger.info("Created first user: test_user")


async def get_session():
    async with async_session() as session:
        yield session
