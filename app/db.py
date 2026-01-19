from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import select

from app.config import settings
from app.models import metadata, User

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def create_first_user():
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.all()

        if not users:
            first_user = User(
                username="test_user",
                api_key="test",
                password_hash="hashed_password_here",
            )
            session.add(first_user)
            await session.commit()
            print("Created first user: test_user")
        else:
            print(f"Database already has {len(users)} user(s)")


async def get_session():
    async with async_session() as session:
        yield session
