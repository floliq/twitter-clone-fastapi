from pydantic import BaseModel


class FollowSchema(BaseModel):
    id: int
    name: str
