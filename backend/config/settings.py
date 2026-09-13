import os
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ManakSetu API"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Security & CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ]
    MAX_REQUEST_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB

    # Modes
    DEMO_MODE: bool = True
    STRICT_CITATION_GUARDRAIL: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./data/bis_assistant.db"

    # Qdrant Vector Store
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_STORAGE_PATH: str = "./data/qdrant"
    QDRANT_COLLECTION_NAME: str = "bis_standards_chunks"

    # LLM Settings
    LLM_PROVIDER: str = "gemini"  # "gemini", "openai", "ollama", "demo"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"

    # Embeddings
    EMBEDDING_PROVIDER: str = "tfidf_semantic"  # "tfidf_semantic", "gemini", "openai", "local"
    EMBEDDING_DIMENSION: int = 384

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
