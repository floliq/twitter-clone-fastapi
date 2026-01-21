from app.repositories.user import UserRepository
from app.schemas.user import UserMe, UserMeResponse


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @staticmethod
    async def get_me(user):
        user_data = UserMeResponse(id=user.id, name=user.username, following=[], followers=[])

        return UserMe(result=True, user=user_data)
