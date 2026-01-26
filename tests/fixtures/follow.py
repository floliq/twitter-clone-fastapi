import pytest
from app.models import Follow


@pytest.fixture
async def sample_follow_by_sample_user(session, sample_user, another_user):
    follow = Follow(
        user_id=sample_user.id,
        follow_user_id=another_user.id,
    )

    session.add(follow)
    await session.commit()
    await session.refresh(follow)

    return follow


@pytest.fixture
async def sample_follow_by_another_user(session, sample_user, another_user):
    follow = Follow(
        user_id=another_user.id,
        follow_user_id=sample_user.id,
    )

    session.add(follow)
    await session.commit()
    await session.refresh(follow)

    return follow
