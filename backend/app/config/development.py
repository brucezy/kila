from base import BaseConfig
from pydantic_settings import SettingsConfigDict


class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""

    environment: str = "development"
    debug: bool = True

    # Database
    mysql_database: str = "ai_prompts_dev"
    mysql_pool_size: int = 5

    # Logging - More verbose in dev
    log_level: str = "DEBUG"

    # CORS - Allow all in development
    allowed_origins: list[str] = ["*"]

    # Rate limiting - Disabled in dev
    rate_limit_enabled: bool = False

    # AI Model - Use cheaper/faster model in dev if needed
    # ai_model: str = "claude-haiku-4-5-20251001"  # Uncomment for cheaper dev testing

    model_config = SettingsConfigDict(
        env_file=".env.development",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
