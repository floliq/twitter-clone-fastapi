from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import func, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models import Attachment, Follow, Like, Tweet
from app.schemas.tweet import TweetCreate


class TweetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_tweets_by_author(self, author_id: int):
        following_subquery = (
            select(Follow.follow_user_id).where(Follow.user_id == author_id).union_all(select(literal(author_id)))
        )

        query = (
            select(Tweet)
            .where(Tweet.author_id.in_(following_subquery))  # type: ignore[attr-defined]
            .outerjoin(Like)
            .group_by(Tweet.id)  # type: ignore[arg-type]
            .order_by(
                func.count(Like.id).desc(),  # type: ignore[arg-type]
                Tweet.id.desc(),  # type: ignore[union-attr]
            )
            .options(
                selectinload(Tweet.attachments),  # type: ignore[arg-type]
                selectinload(Tweet.author),  # type: ignore[arg-type]
                selectinload(Tweet.likes),  # type: ignore[arg-type]
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

    async def delete_tweet(self, tweet_id: int):
        query = (
            select(Tweet)
            .where(Tweet.id == tweet_id)
            .options(
                selectinload(Tweet.attachments),  # type: ignore[arg-type]
            )
        )
        result = await self.session.execute(query)
        tweet = result.scalar_one_or_none()

        if not tweet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")

        app_path = Path("app")

        for attachment in tweet.attachments:
            file_path = app_path / attachment.path
            if file_path.exists():
                file_path.unlink()

        await self.session.delete(tweet)
        await self.session.commit()

        return True

    async def like_tweet(self, tweet_id: int, user_id: int):
        query = select(Like).where(Like.tweet_id == tweet_id, Like.user_id == user_id)

        result = await self.session.execute(query)
        like = result.scalar_one_or_none()

        if like:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Like is already exists")

        new_like = Like(
            tweet_id=tweet_id,
            user_id=user_id,
        )

        self.session.add(new_like)
        await self.session.commit()

        return True

    async def remove_like_tweet(self, tweet_id: int, user_id: int):
        query = select(Like).where(Like.tweet_id == tweet_id, Like.user_id == user_id)

        result = await self.session.execute(query)
        like = result.scalar_one_or_none()

        if not like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")

        await self.session.delete(like)
        await self.session.commit()

        return True
