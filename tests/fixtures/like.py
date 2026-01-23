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
