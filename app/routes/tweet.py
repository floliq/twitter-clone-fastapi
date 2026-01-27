from fastapi import APIRouter, status

from app.depends import CurrentUser, TweetServiceAnnotation
from app.schemas.response import Response, ResponseError
from app.schemas.tweet import TweetCreate, TweetCreateResponse, TweetResponse

tweet_router = APIRouter(prefix="/api/tweets")


@tweet_router.get(
    "",
    summary="Get list of tweets",
    description=(
        "Retrieve a feed of tweets from the current user and their subscriptions, "
        "sorted by number of likes and creation time (descending)."
    ),
    response_model=TweetResponse,
    responses={
        200: {
            "description": "Successful response, list of tweets.",
        },
        401: {
            "description": "User is not authorized.",
            "model": ResponseError,
            "content": {
                "application/json": {
                    "examples": {
                        "no_api_key": {
                            "summary": "No API key",
                            "value": {
                                "result": False,
                                "error_type": "auth_error",
                                "error_message": "API key is required",
                            },
                        },
                        "invalid_api_key": {
                            "summary": "Invalid API key",
                            "value": {"result": False, "error_type": "auth_error", "error_message": "User not found"},
                        },
                    }
                }
            },
        },
    },
)
async def get_tweets(
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.get_all_tweets(current_user.id)


@tweet_router.post(
    "",
    summary="Create new tweet",
    description="Create a new tweet. Content must not be empty. Optional attachments (media).",
    response_model=TweetCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Tweet created successfully.",
        },
        400: {
            "description": "Invalid data or empty tweet content.",
            "content": {
                "application/json": {
                    "examples": {
                        "empty_content": {
                            "summary": "Empty tweet content",
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Tweet content cannot be empty",
                            },
                        },
                    }
                }
            },
        },
    },
)
async def create_tweet(
    tweet_data: TweetCreate,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.create_tweet(tweet_data, current_user.id)


@tweet_router.delete(
    "/{tweet_id}",
    summary="Delete tweet",
    description=("Delete a tweet by its ID. Note: all attached files will also be removed."),
    response_model=Response,
    responses={
        200: {
            "description": "Tweet deleted successfully.",
            "content": {
                "application/json": {
                    "example": {"result": True},
                }
            },
        },
        404: {
            "description": "Tweet not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "tweet_not_found": {
                            "summary": "Tweet not found",
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Tweet not found",
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
async def delete_tweet(
    tweet_id: int,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.delete_tweet(tweet_id)


@tweet_router.post(
    "/{tweet_id}/likes",
    summary="Like tweet",
    description="Add a like to a tweet as the current user.",
    response_model=Response,
    responses={
        200: {"description": "Like added successfully."},
        400: {
            "description": "Like already exists.",
            "content": {
                "application/json": {
                    "examples": {
                        "like_exists": {
                            "summary": "Like already exists",
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Like is already existsd",
                            },
                        }
                    }
                }
            },
        },
        401: {
            "description": "User is not authorized.",
        },
        404: {
            "description": "Tweet not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "tweet_not_found": {
                            "summary": "Tweet not found",
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Tweet not found",
                            },
                        }
                    }
                }
            },
        },
    },
)
async def like_tweet(
    tweet_id: int,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.like_tweet(tweet_id, current_user.id)


@tweet_router.delete(
    "/{tweet_id}/likes",
    summary="Remove like from tweet",
    description="Remove a like from a tweet as the current user.",
    response_model=Response,
    responses={
        200: {"description": "Like removed successfully."},
        404: {
            "description": "Like not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "like_not_found": {
                            "summary": "Like not found",
                            "value": {
                                "result": False,
                                "error_type": "validation_error",
                                "error_message": "Like not found",
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
async def remove_like_tweet(
    tweet_id: int,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.remove_like_tweet(tweet_id, current_user.id)
