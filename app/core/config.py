from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "AI Security Copilot"

    ENVIRONMENT: str = "development"

    DATABASE_URL: str = Field(...)

    JWT_SECRET: str  = Field(...)

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    AZURE_OPENAI_ENDPOINT: str | None = None

    AZURE_OPENAI_API_KEY: str | None = None

    AZURE_OPENAI_API_VERSION: str | None = None

    AZURE_OPENAI_DEPLOYMENT: str | None = None

    AZURE_OPENAI_DEPLOYMENT_NAME: str | None = None

    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str | None = None

    REDIS_URL: str = "redis://localhost:6379"

    LANGCHAIN_TRACING_V2: bool = False

    LANGCHAIN_API_KEY: str | None = None

    LANGCHAIN_PROJECT: str = "ai-security-copilot"

    LOG_LEVEL: str = "INFO"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


@lru_cache
def get_settings() -> Settings:

    return Settings()


settings: Settings = get_settings()
