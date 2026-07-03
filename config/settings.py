"""Application settings and configuration management."""

from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from typing import Optional, Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_env: Literal["development", "staging", "production"] = Field(
        default="development", env="APP_ENV"
    )
    app_debug: bool = Field(default=False, env="APP_DEBUG")
    app_log_level: str = Field(default="INFO", env="APP_LOG_LEVEL")

    # LLM Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(default=2000, env="OPENAI_MAX_TOKENS")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small", env="OPENAI_EMBEDDING_MODEL"
    )

    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(
        default="claude-3-opus-20240229", env="ANTHROPIC_MODEL"
    )

    # Embeddings
    embeddings_provider: Literal["openai", "huggingface", "mock"] = Field(
        default="openai", env="EMBEDDINGS_PROVIDER"
    )
    huggingface_model: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        env="HUGGINGFACE_MODEL",
    )

    # Vector Database
    vector_db_type: Literal["chroma", "weaviate", "mock"] = Field(
        default="chroma", env="VECTOR_DB_TYPE"
    )
    vector_db_path: str = Field(default="./data/vector_store", env="VECTOR_DB_PATH")
    weaviate_url: str = Field(default="http://localhost:8080", env="WEAVIATE_URL")

    # Scraper Configuration
    scraper_agenzia_entrate_url: str = Field(
        default="https://www.agenziaentrate.gov.it",
        env="SCRAPER_AGENZIA_ENTRATE_URL",
    )
    scraper_timeout: int = Field(default=30, env="SCRAPER_TIMEOUT")
    scraper_retries: int = Field(default=3, env="SCRAPER_RETRIES")
    scraper_rate_limit: float = Field(default=1.0, env="SCRAPER_RATE_LIMIT")

    # Knowledge Base
    kb_data_path: str = Field(default="./data/knowledge_base", env="KB_DATA_PATH")
    kb_backup_path: str = Field(
        default="./data/backups", env="KB_BACKUP_PATH"
    )

    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")

    # Logging
    log_path: str = Field(default="./logs", env="LOG_PATH")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: Literal["json", "text"] = Field(default="json", env="LOG_FORMAT")

    # Feature Flags
    feature_news_scraper: bool = Field(default=True, env="FEATURE_NEWS_SCRAPER")
    feature_semantic_search: bool = Field(
        default=True, env="FEATURE_SEMANTIC_SEARCH"
    )
    feature_risk_analyzer: bool = Field(default=True, env="FEATURE_RISK_ANALYZER")
    feature_daily_briefing: bool = Field(default=True, env="FEATURE_DAILY_BRIEFING")

    # Performance
    max_search_results: int = Field(default=10, env="MAX_SEARCH_RESULTS")
    embedding_batch_size: int = Field(default=32, env="EMBEDDING_BATCH_SIZE")
    llm_request_timeout: int = Field(default=60, env="LLM_REQUEST_TIMEOUT")
    vector_store_batch_size: int = Field(
        default=100, env="VECTOR_STORE_BATCH_SIZE"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def get_vector_db_path(self) -> Path:
        """Get vector database path as Path object."""
        path = Path(self.vector_db_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_kb_data_path(self) -> Path:
        """Get knowledge base data path as Path object."""
        path = Path(self.kb_data_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_log_path(self) -> Path:
        """Get logging path as Path object."""
        path = Path(self.log_path)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Singleton instance
settings = Settings()
