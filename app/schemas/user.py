from pydantic import BaseModel, Field

from app.schemas.response import Response


class UserResponse(BaseModel):
    id: int
    name: str
    followers: list[dict] = Field(default_factory=list)
    following: list[dict] = Field(default_factory=list)


class UserMe(Response):
    user: UserResponse


class AuthorSchema(BaseModel):
    id: int
    name: str
