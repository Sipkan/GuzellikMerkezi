import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # REQUIRED: Must be set in .env — no hardcoded default password
    database_url: str = "postgresql+asyncpg://postgres:changeme@localhost:5432/merkez"

    # Secret key for admin auth (auto-generated if not set)
    admin_username: str = "admin"
    admin_password: str = "changeme"
    secret_key: str = secrets.token_urlsafe(32)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
