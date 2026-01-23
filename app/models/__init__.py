from sqlmodel import SQLModel

from app.models.attachment import Attachment
from app.models.like import Like
from app.models.tweet import Tweet
from app.models.user import User

metadata = SQLModel.metadata  # NOQA RUF067

__all__ = ["Attachment", "Like", "Tweet", "User", "metadata"]
