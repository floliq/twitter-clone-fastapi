from fastapi import APIRouter, status

from app.depends import CurrentUser, UserServiceAnnotation
from app.exception_handlers import CustomHTTPException
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
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "User not found",
                            },
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
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Can't follow to yourself",
                            },
                        },
                        "follow_exists": {
                            "summary": "Follow already exists",
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Follow is already exists",
                            },
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
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_type="validation_error",
            error_message="Can't follow to yourself",
        )

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
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Can't unfollow to yourself",
                            },
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
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Follow not found",
                            },
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
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_type="validation_error",
            error_message="Can't unfollow to yourself",
        )

    return await user_service.unfollow_user(follow_id, current_user.id)
