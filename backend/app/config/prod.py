from pydantic_settings import SettingsConfigDict
from app.config.base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production environment configuration"""

    environment: str = "production"
    debug: bool = False

    # Database
    mysql_database: str = "ai_prompts"
    mysql_pool_size: int = 20
    mysql_max_overflow: int = 40

    # Logging - Only important stuff
    log_level: str = "WARNING"

    # CORS - Strict domain whitelist
    allowed_origins: list[str] = [
        "https://yourapp.com",
        "https://www.yourapp.com",
        "https://api.yourapp.com"
    ]

    # Rate limiting - Strict limits
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60

    # AI Settings - Production model
    ai_model: str = "claude-sonnet-4-5-20250929"
    ai_timeout: int = 60  # Longer timeout in production

    # Security - Must be set in environment
    # These will raise validation errors if not provided
    secret_key: str  # No default - must be in .env.production

    model_config = SettingsConfigDict(
        env_file=".env.prod",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
