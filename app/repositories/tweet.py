from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models import Attachment, Tweet
from app.schemas.tweet import TweetCreate


class TweetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_tweets_by_author(self, author_id: int):
        query = (
            select(Tweet)
            .where(Tweet.author_id == author_id)
            .options(
                selectinload(Tweet.attachments),  # type: ignore[arg-type]
                selectinload(Tweet.author),  # type: ignore[arg-type]
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_new_tweet(self, tweet_data: TweetCreate, author_id: int):
        new_tweet = Tweet(content=tweet_data.tweet_data, author_id=author_id)

        self.session.add(new_tweet)
        await self.session.commit()
        await self.session.refresh(new_tweet)

        attachments_ids = tweet_data.tweet_media_ids

        for attachment_id in attachments_ids:
            attachment = await self.session.get(Attachment, attachment_id)
            if attachment and new_tweet.id is not None:
                attachment.tweet_id = new_tweet.id
                self.session.add(attachment)

        await self.session.commit()
        await self.session.refresh(new_tweet)

        return new_tweet
