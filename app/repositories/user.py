from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import User


@dataclass
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)

        result = await self.session.execute(query)

        user = result.scalar_one_or_none()

        return user
