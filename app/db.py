import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import select

from app.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_first_user():
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.all()

        if not users:
            first_user = User(
                username="test_user",
                api_key="test",
            )
            session.add(first_user)
            await session.commit()
            logger.info("Created first user: test_user")
        else:
            logger.info(f"Database already has {len(users)} user(s)")


async def get_session():
    async with async_session() as session:
        yield session
