from typing import Annotated, Any

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.db import get_session
from app.models import Follow, User
from app.repositories.media import MediaRepository
from app.repositories.tweet import TweetRepository
from app.repositories.user import UserRepository
from app.services.media import MediaService
from app.services.tweet import TweetService
from app.services.user import UserService

DbSession = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    session: DbSession,
    api_key: Annotated[str | None, Header(alias="api-key")] = None,
):
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key is required")

    query = (
        select(User)
        .where(User.api_key == api_key)
        .options(
            selectinload(User.followers_relations).selectinload(Follow.follower),  # type: ignore[arg-type]
            selectinload(User.following_relations).selectinload(Follow.following_user),  # type: ignore[arg-type]
        )
    )
    user_result = await session.execute(query)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def get_user_service(
    session: DbSession,
):
    repository = UserRepository(session)
    return UserService(repository)


def get_tweet_service(
    session: DbSession,
):
    repository = TweetRepository(session)
    return TweetService(repository)


def get_media_service(
    session: DbSession,
):
    repository = MediaRepository(session)
    return MediaService(repository)


CurrentUser = Annotated[Any, Depends(get_current_user)]
MediaServiceAnnotation = Annotated[MediaService, Depends(get_media_service)]
TweetServiceAnnotation = Annotated[TweetService, Depends(get_tweet_service)]
UserServiceAnnotation = Annotated[UserService, Depends(get_user_service)]
