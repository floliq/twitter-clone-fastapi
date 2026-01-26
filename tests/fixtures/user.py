import pytest
from app.models import User


@pytest.fixture
async def sample_user(session):
    user = User(
        username="test_user",
        api_key="test",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture
async def another_user(session):
    user = User(
        username="another_user",
        api_key="another",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
