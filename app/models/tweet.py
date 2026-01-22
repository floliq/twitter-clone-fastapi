from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Tweet(SQLModel, table=True):
    __tablename__ = "tweets"

    id: int | None = Field(default=None, primary_key=True)
    content: str
    author_id: int = Field(foreign_key="users.id", nullable=False)

    author: Optional["User"] = Relationship(back_populates="tweets")  # type: ignore[name-defined]  # NOQA F821

    attachments: list["Attachment"] = Relationship(  # type: ignore[name-defined]  # NOQA F821
        back_populates="tweet", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self):
        return f"Tweet: {self.author_id} {self.content}"
