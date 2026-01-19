from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.db import get_session
from app.models import User
from sqlmodel import select

router = APIRouter(prefix="/api/users")


@router.get("/me")
async def get_me(
    api_key: str = Header(..., alias="api-key"),
    session: AsyncSession = Depends(get_session),
):
    query = select(User).where(User.api_key == api_key)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    user_data = {"id": user.id, "name": user.username, "followers": [], "following": []}

    return {"result": "true", "user": user_data}
