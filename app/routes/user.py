from fastapi import APIRouter, Depends, HTTPException, status

from app.depends import get_current_user, get_user_service
from app.services.user import UserService

user_router = APIRouter(prefix="/api/users")


@user_router.get("/me")
async def get_me(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_me(current_user)


@user_router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user_by_id(user_id)


@user_router.post("/{follow_id}/follow")
async def follow_user(
    follow_id: int,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    if follow_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't follow to yourself")

    return await user_service.follow_user(follow_id, current_user.id)


@user_router.delete("/{follow_id}/follow")
async def unfollow_user(
    follow_id: int,
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    if follow_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't unfollow to yourself")

    return await user_service.unfollow_user(follow_id, current_user.id)
