from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://humanizer:humanizer@db:5432/humanizer"

    # Security
    secret_key: str = "change-me-to-a-random-string"

    # CORS — accepts comma-separated string or "*"
    cors_origins: str = "http://localhost:3000"

    # Text limits
    max_text_length: int = 50_000

    # LLM APIs
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from string."""
        if self.cors_origins == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
