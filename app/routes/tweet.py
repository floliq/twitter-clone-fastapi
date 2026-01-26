from fastapi import APIRouter

from app.depends import CurrentUser, TweetServiceAnnotation
from app.schemas.tweet import TweetCreate

tweet_router = APIRouter(prefix="/api/tweets")


@tweet_router.get("")
async def get_tweets(current_user: CurrentUser, tweet_service: TweetServiceAnnotation):
    return await tweet_service.get_all_tweets(current_user.id)


@tweet_router.post("")
async def create_tweet(
    tweet_data: TweetCreate,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.create_tweet(tweet_data, current_user.id)


@tweet_router.delete("/{tweet_id}")
async def delete_tweet(
    tweet_id: int,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.delete_tweet(tweet_id)


@tweet_router.post("/{tweet_id}/likes")
async def like_tweet(
    tweet_id: int,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.like_tweet(tweet_id, current_user.id)


@tweet_router.delete("/{tweet_id}/likes")
async def remove_like_tweet(
    tweet_id: int,
    current_user: CurrentUser,
    tweet_service: TweetServiceAnnotation,
):
    return await tweet_service.remove_like_tweet(tweet_id, current_user.id)
