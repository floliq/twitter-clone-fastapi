from sqlmodel import SQLModel

from app.models.tweet import Tweet
from app.models.user import User

metadata = SQLModel.metadata  # NOQA RUF067

__all__ = ["Tweet", "User", "metadata"]
