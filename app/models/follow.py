from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class Follow(SQLModel, table=True):
    __tablename__ = "follows"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    follow_user_id: int = Field(foreign_key="users.id", nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "follow_user_id", name="uq_user_follow"),)

    follower: Optional["User"] = Relationship(  # type: ignore[name-defined]  # NOQA F821
        sa_relationship_kwargs={"foreign_keys": "[Follow.user_id]", "primaryjoin": "User.id == Follow.user_id"}
    )

    following_user: Optional["User"] = Relationship(  # type: ignore[name-defined]  # NOQA F821
        sa_relationship_kwargs={
            "foreign_keys": "[Follow.follow_user_id]",
            "primaryjoin": "User.id == Follow.follow_user_id",
        }
    )

    def __repr__(self):
        return f"Follow: {self.user_id} {self.follow_user_id}"
