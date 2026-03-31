from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = "postgresql+asyncpg://postgres:123456@localhost:5432/merkez"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
