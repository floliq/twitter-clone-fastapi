from pydantic import BaseModel, Field

from app.schemas.response import Response


class UserMeResponse(BaseModel):
    id: int
    name: str
    followers: list[dict] = Field(default_factory=list)
    following: list[dict] = Field(default_factory=list)


class UserMe(Response):
    user: UserMeResponse


class AuthorSchema(BaseModel):
    id: int
    name: str
