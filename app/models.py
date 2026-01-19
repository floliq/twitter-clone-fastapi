from datetime import datetime

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str
    api_key: str
    created_at: datetime = Field(default=datetime.now())

    def __repr__(self):
        return f"User: {self.username}"


metadata = SQLModel.metadata
