from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "CORE Studio"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://core_user:core_pass@localhost:5432/core_studio"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Auth
    JWT_SECRET: str = "change_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # AI Models
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    FIGMA_API_KEY: str = ""

    # Model Routing Thresholds (complexity score 1-10)
    DEFAULT_FAST_MODEL: str = "claude-haiku-4-5-20251001"
    DEFAULT_STANDARD_MODEL: str = "claude-sonnet-4-6"
    DEFAULT_ADVANCED_MODEL: str = "claude-opus-4-8"
    COMPLEXITY_FAST_THRESHOLD: int = 3       # 1-3 → Haiku
    COMPLEXITY_STANDARD_THRESHOLD: int = 7   # 4-7 → Sonnet, 8-10 → Opus

    # Storage
    UPLOADS_DIR: str = "./uploads"
    KNOWLEDGE_DIR: str = "./knowledge"
    MAX_UPLOAD_SIZE_MB: int = 50

    # Embedding
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
