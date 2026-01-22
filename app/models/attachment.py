from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Attachment(SQLModel, table=True):
    __tablename__ = "attachments"

    id: int | None = Field(default=None, primary_key=True)
    path: str
    tweet_id: int = Field(foreign_key="tweets.id", nullable=True)

    tweet: Optional["Tweet"] = Relationship(back_populates="attachments")  # type: ignore[name-defined]  # NOQA F821

    def __repr__(self):
        return f"Attachment: {self.path}"
