import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL", None)
POSTGRES_DB = os.getenv("POSTGRES_DB", None)
POSTGRES_USER = os.getenv("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", None)

if POSTGRES_URL is None or POSTGRES_DB is None or POSTGRES_USER is None:
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    database_url: str = DATABASE_URL


settings = Settings()
