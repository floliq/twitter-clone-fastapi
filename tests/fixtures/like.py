import pytest
from app.models import Like


@pytest.fixture
async def sample_like_by_sample_user(session, sample_user, sample_tweet):
    like = Like(
        user_id=sample_user.id,
        tweet_id=sample_tweet.id,
    )

    session.add(like)
    await session.commit()
    await session.refresh(like)

    return like


@pytest.fixture
async def sample_like_by_another_user(session, another_user, sample_tweet):
    like = Like(
        user_id=another_user.id,
        tweet_id=sample_tweet.id,
    )

    session.add(like)
    await session.commit()
    await session.refresh(like)

    return like


@pytest.fixture
async def sample_like_to_another_user_tweet(session, sample_user, sample_tweet_by_another_user):
    like = Like(
        user_id=sample_user.id,
        tweet_id=sample_tweet_by_another_user.id,
    )

    session.add(like)
    await session.commit()
    await session.refresh(like)

    return like
