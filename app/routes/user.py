from fastapi import APIRouter, Depends

from app.depends import get_current_user, get_user_service
from app.services.user import UserService

user_router = APIRouter(prefix="/api/users")


@user_router.get("/me")
async def get_me(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_me(current_user)
