from fastapi import HTTPException, status

from app.repositories.tweet import TweetRepository
from app.schemas.response import Response
from app.schemas.tweet import TweetCreate, TweetCreateResponse, TweetResponse, TweetSchema
from app.schemas.user import AuthorSchema


class TweetService:
    def __init__(self, repository: TweetRepository):
        self.repository = repository

    async def get_all_tweets(self, author_id: int):
        tweets = await self.repository.get_all_tweets_by_author(author_id)

        tweets_data = []
        for tweet in tweets:
            author_schema = AuthorSchema(id=tweet.author.id, name=tweet.author.username)

            tweet_schema = TweetSchema(
                id=tweet.id,
                content=tweet.content,
                author=author_schema,
                attachments=[attachment.path for attachment in tweet.attachments],
                likes=[],
            )
            tweets_data.append(tweet_schema)

        return TweetResponse(result=True, tweets=tweets_data)

    async def create_tweet(self, tweet_data: TweetCreate, author_id: int):
        if not tweet_data.tweet_data.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet content cannot be empty")

        tweet = await self.repository.create_new_tweet(tweet_data=tweet_data, author_id=author_id)

        return TweetCreateResponse(result=True, tweet_id=tweet.id)

    async def delete_tweet(self, tweet_id: int):
        tweet = await self.repository.delete_tweet(tweet_id)

        return Response(result=tweet)
