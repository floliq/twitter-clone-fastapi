from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db import get_session
from app.models import User

router = APIRouter(prefix="/api/users")


@router.get("/me")
async def get_me(
    api_key: Annotated[str, Header(..., alias="api-key")],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    query = select(User).where(User.api_key == api_key)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    user_data: dict[str, Any] = {"id": user.id, "name": user.username, "followers": [], "following": []}

    return {"result": "true", "user": user_data}
