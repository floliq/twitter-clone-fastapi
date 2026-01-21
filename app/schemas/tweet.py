from pydantic import BaseModel, Field

from app.schemas.response import Response
from app.schemas.user import AuthorSchema


class TweetSchema(BaseModel):
    id: int
    content: str
    author: AuthorSchema
    attachments: list[str] = Field(default_factory=list)
    likes: list[dict] = Field(default_factory=list)


class TweetResponse(Response):
    tweets: list[TweetSchema]


class TweetCreateResponse(Response):
    tweet_id: int


class TweetCreate(BaseModel):
    tweet_data: str
