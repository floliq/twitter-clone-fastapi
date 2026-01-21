import pytest
from app.models import Tweet


@pytest.fixture
async def sample_tweet(session, sample_user):
    tweet = Tweet(
        content="Test content",
        author_id=sample_user.id,
    )

    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)

    return tweet


@pytest.fixture
async def another_tweet(session, sample_user):
    tweet = Tweet(
        content="Test content 2",
        author_id=sample_user.id,
    )

    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)

    return tweet
