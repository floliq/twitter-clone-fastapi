from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class Like(SQLModel, table=True):
    __tablename__ = "likes"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    tweet_id: int = Field(foreign_key="tweets.id", nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="uq_user_tweet"),)

    user: Optional["User"] = Relationship(back_populates="likes")  # type: ignore[name-defined]  # NOQA F821
    tweet: Optional["Tweet"] = Relationship(back_populates="likes")  # type: ignore[name-defined]  # NOQA F821

    def __repr__(self):
        return f"Like: {self.user_id} {self.tweet_id}"
