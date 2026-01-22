import pytest
from app.models import Attachment


@pytest.fixture
async def sample_attachment(session, sample_tweet):
    attachment = Attachment(
        path="/media/test_file1.png",
        tweet_id=sample_tweet.id,
    )

    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)

    return attachment


@pytest.fixture
async def another_attachment(session, sample_tweet):
    attachment = Attachment(
        path="/media/test_file2.png",
        tweet_id=sample_tweet.id,
    )

    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)

    return attachment


@pytest.fixture
async def attachment_without_tweet(session):
    attachment = Attachment(
        path="/media/test_file2.png",
        tweet_id=None,
    )

    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)

    return attachment
