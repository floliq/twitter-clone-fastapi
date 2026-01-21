from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db import get_session
from app.models import User
from app.repositories.tweet import TweetRepository
from app.repositories.user import UserRepository
from app.services.tweet import TweetService
from app.services.user import UserService


async def get_current_user(
    api_key: str | None = Header(None, alias="api-key"),
    session: AsyncSession = Depends(get_session),
):
    if api_key is None:
        raise HTTPException(status_code=401, detail="API key is required")

    query = select(User).where(User.api_key == api_key)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_user_service(
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    return UserService(repository)


def get_tweet_service(
    session: AsyncSession = Depends(get_session),
):
    repository = TweetRepository(session)
    return TweetService(repository)
