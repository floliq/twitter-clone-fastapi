from fastapi import APIRouter, Depends

from app.depends import get_current_user, get_tweet_service
from app.schemas.tweet import TweetCreate
from app.services.tweet import TweetService

tweet_router = APIRouter(prefix="/api/tweets")


@tweet_router.get("")
async def get_tweets(current_user=Depends(get_current_user), tweet_service: TweetService = Depends(get_tweet_service)):
    return await tweet_service.get_all_tweets(current_user.id)


@tweet_router.post("")
async def create_tweet(
    tweet_data: TweetCreate,
    current_user=Depends(get_current_user),
    tweet_service: TweetService = Depends(get_tweet_service),
):
    return await tweet_service.create_tweet(tweet_data, current_user.id)


@tweet_router.delete("/{tweet_id}")
async def delete_post(
    tweet_id: int,
    current_user=Depends(get_current_user),
    tweet_service: TweetService = Depends(get_tweet_service),
):
    return await tweet_service.delete_tweet(tweet_id)
