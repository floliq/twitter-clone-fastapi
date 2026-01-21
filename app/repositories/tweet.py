from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Tweet


class TweetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_tweets_by_author(self, author_id: int):
        query = select(Tweet).where(Tweet.author_id == author_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_new_tweet(self, content: str, author_id: int):
        new_tweet = Tweet(content=content, author_id=author_id)

        self.session.add(new_tweet)
        await self.session.commit()
        await self.session.refresh(new_tweet)

        return new_tweet
