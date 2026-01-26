from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.follow import FollowSchema
from app.schemas.response import Response
from app.schemas.user import UserMe, UserResponse


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @staticmethod
    async def get_me(user):
        followers_data = [
            FollowSchema(id=rel.follower.id, name=rel.follower.username) for rel in user.followers_relations
        ]
        following_data = [
            FollowSchema(id=rel.following_user.id, name=rel.following_user.username) for rel in user.following_relations
        ]

        user_data = UserResponse(id=user.id, name=user.username, following=following_data, followers=followers_data)

        return UserMe(result=True, user=user_data)

    async def get_user_by_id(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        followers_data = [
            FollowSchema(id=rel.follower.id, name=rel.follower.username) for rel in user.followers_relations
        ]
        following_data = [
            FollowSchema(id=rel.following_user.id, name=rel.following_user.username) for rel in user.following_relations
        ]

        user_data = UserResponse(id=user.id, name=user.username, following=following_data, followers=followers_data)

        return UserMe(result=True, user=user_data)

    async def follow_user(self, follow_id: int, user_id):
        result = await self.repository.follow_user(follow_id, user_id)

        return Response(result=result)

    async def unfollow_user(self, follow_id: int, user_id):
        result = await self.repository.unfollow_user(follow_id, user_id)

        return Response(result=result)
