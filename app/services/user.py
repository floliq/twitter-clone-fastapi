from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.user import UserMe, UserResponse


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @staticmethod
    async def get_me(user):
        user_data = UserResponse(id=user.id, name=user.username, following=[], followers=[])

        return UserMe(result=True, user=user_data)

    async def get_user_by_id(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")

        user_data = UserResponse(id=user.id, name=user.username, following=[], followers=[])

        return UserMe(result=True, user=user_data)
