import os
from functools import lru_cache
from app.config.base import BaseConfig
from app.config.development import DevelopmentConfig
from app.config.beta import BetaConfig
from app.config.prod import ProductionConfig

# Mapping of environment names to config classes
config_by_name = {
    "development": DevelopmentConfig,
    "dev": DevelopmentConfig,
    "beta": BetaConfig,
    "staging": BetaConfig,
    "production": ProductionConfig,
    "prod": ProductionConfig,
}


@lru_cache()
def get_settings() -> BaseConfig:
    """
    Get settings based on ENVIRONMENT variable.
    Cached to avoid reloading on every call.

    Priority order for determining environment:
    1. ENVIRONMENT env var
    2. APP_ENV env var
    3. Default to 'development'
    """
    env = os.getenv("ENVIRONMENT") or os.getenv("APP_ENV") or "development"
    env = env.lower()

    config_class = config_by_name.get(env, DevelopmentConfig)

    return config_class()


# Convenience function to get current environment name
def get_environment() -> str:
    """Get the current environment name"""
    return get_settings().environment


# Export settings instance
settings = get_settings()

# Export all config classes for testing
__all__ = [
    "settings",
    "get_settings",
    "get_environment",
    "BaseConfig",
    "DevelopmentConfig",
    "BetaConfig",
    "ProductionConfig",
]
