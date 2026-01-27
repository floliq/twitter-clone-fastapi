from fastapi import APIRouter, HTTPException, status

from app.depends import CurrentUser, UserServiceAnnotation
from app.schemas.response import Response
from app.schemas.user import UserMe

user_router = APIRouter(prefix="/api/users")


@user_router.get(
    "/me",
    summary="Get information about the current user",
    description="Retrieve the authenticated user's profile information including followers and following.",
    response_model=UserMe,
    responses={
        200: {"description": "Successful response, user profile returned."},
        401: {
            "description": "User is not authorized.",
        },
    },
)
async def get_me(
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    return await user_service.get_me(current_user)


@user_router.get(
    "/{user_id}",
    summary="Get user by ID",
    description="Retrieve a user's profile information, including followers and following, by user ID.",
    response_model=UserMe,
    responses={
        200: {"description": "Successful response, user profile returned."},
        404: {
            "description": "User not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "user_not_found": {
                            "summary": "User not found",
                            "value": {"detail": "User not found"},
                        }
                    }
                }
            },
        },
        401: {
            "description": "User is not authorized.",
        },
    },
)
async def get_user_by_id(
    user_id: int,
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    return await user_service.get_user_by_id(user_id)


@user_router.post(
    "/{follow_id}/follow",
    summary="Follow a user",
    description="Follow another user by their user ID. Cannot follow yourself.",
    response_model=Response,
    responses={
        200: {"description": "Followed user successfully."},
        400: {
            "description": "Cannot follow yourself or follow already exists.",
            "content": {
                "application/json": {
                    "examples": {
                        "self_follow": {
                            "summary": "Attempt to follow self",
                            "value": {"detail": "Can't follow to yourself"},
                        },
                        "follow_exists": {
                            "summary": "Follow already exists",
                            "value": {"detail": "Follow is already exists"},
                        },
                    }
                }
            },
        },
        401: {
            "description": "User is not authorized.",
        },
    },
)
async def follow_user(
    follow_id: int,
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    if follow_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't follow to yourself")

    return await user_service.follow_user(follow_id, current_user.id)


@user_router.delete(
    "/{follow_id}/follow",
    summary="Unfollow a user",
    description="Unfollow a user by their user ID. Cannot unfollow yourself.",
    response_model=Response,
    responses={
        200: {"description": "Unfollowed user successfully."},
        400: {
            "description": "Cannot unfollow yourself.",
            "content": {
                "application/json": {
                    "examples": {
                        "self_unfollow": {
                            "summary": "Attempt to unfollow self",
                            "value": {"detail": "Can't unfollow to yourself"},
                        }
                    }
                }
            },
        },
        404: {
            "description": "Follow not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "follow_not_found": {
                            "summary": "Follow not found",
                            "value": {"detail": "Follow not found"},
                        }
                    }
                }
            },
        },
        401: {
            "description": "User is not authorized.",
        },
    },
)
async def unfollow_user(
    follow_id: int,
    current_user: CurrentUser,
    user_service: UserServiceAnnotation,
):
    if follow_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't unfollow to yourself")

    return await user_service.unfollow_user(follow_id, current_user.id)
