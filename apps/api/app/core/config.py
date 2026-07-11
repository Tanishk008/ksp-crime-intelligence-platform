from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "change-this-to-a-secure-random-string-in-production"
    APP_CORS_ORIGINS: str = "http://localhost:5173"
    
    # DB (MySQL in Zoho Catalyst)
    DB_PROVIDER: str = "sqlite"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "ksp_intelligence"

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI Config
    LLM_MODEL: str = "claude-sonnet-4-6"
    EMBEDDING_MODEL: str = "paraphrase-multilingual-mpnet-base-v2"
    WHISPER_MODEL_SIZE: str = "large-v3"
    
    # AI Engine URL
    AI_ENGINE_URL: str = "http://localhost:8001/api/v1/reason"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
