from fastapi import APIRouter, HTTPException, status

from app.depends import CurrentUser, UserServiceAnnotation

user_router = APIRouter(prefix="/api/users")


@user_router.get("/me")
async def get_me(
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    return await user_service.get_me(current_user)


@user_router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    return await user_service.get_user_by_id(user_id)


@user_router.post("/{follow_id}/follow")
async def follow_user(
    follow_id: int,
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    if follow_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't follow to yourself")

    return await user_service.follow_user(follow_id, current_user.id)


@user_router.delete("/{follow_id}/follow")
async def unfollow_user(
    follow_id: int,
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    if follow_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't unfollow to yourself")

    return await user_service.unfollow_user(follow_id, current_user.id)
