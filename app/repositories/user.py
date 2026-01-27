from dataclasses import dataclass

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.exception_handlers import CustomHTTPException
from app.models import Follow, User


@dataclass
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int):
        query = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.followers_relations).selectinload(Follow.follower),  # type: ignore[arg-type]
                selectinload(User.following_relations).selectinload(Follow.following_user),  # type: ignore[arg-type]
            )
        )

        query_result = await self.session.execute(query)

        user = query_result.scalar_one_or_none()

        return user

    async def follow_user(self, follow_id: int, user_id: int):
        query = select(Follow).where(Follow.user_id == user_id, Follow.follow_user_id == follow_id)

        query_result = await self.session.execute(query)
        follow = query_result.scalar_one_or_none()

        if follow:
            raise CustomHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_type="validation_error",
                error_message="Follow is already exists",
            )

        new_follow = Follow(
            user_id=user_id,
            follow_user_id=follow_id,
        )

        self.session.add(new_follow)
        await self.session.commit()

        return True

    async def unfollow_user(self, follow_id: int, user_id: int):
        query = select(Follow).where(Follow.user_id == user_id, Follow.follow_user_id == follow_id)

        query_result = await self.session.execute(query)
        follow = query_result.scalar_one_or_none()

        if not follow:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND, error_type="validation_error", error_message="Follow not found"
            )

        await self.session.delete(follow)
        await self.session.commit()

        return True
