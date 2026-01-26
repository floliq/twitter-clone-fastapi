from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str
    api_key: str
    created_at: datetime = Field(default=datetime.now())

    tweets: list["Tweet"] = Relationship(back_populates="author")  # type: ignore[name-defined]  # NOQA F821
    likes: list["Like"] = Relationship(back_populates="user")  # type: ignore[name-defined]  # NOQA F821

    followers_relations: list["Follow"] = Relationship(  # type: ignore[name-defined]  # NOQA F821
        back_populates="following_user",
        sa_relationship_kwargs={
            "foreign_keys": "[Follow.follow_user_id]",
            "primaryjoin": "User.id == Follow.follow_user_id",
        },
    )

    following_relations: list["Follow"] = Relationship(  # type: ignore[name-defined]  # NOQA F821
        back_populates="follower",
        sa_relationship_kwargs={"foreign_keys": "[Follow.user_id]", "primaryjoin": "User.id == Follow.user_id"},
    )

    def __repr__(self):
        return f"User: {self.username}"
