"""Application configuration."""
from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environments."""
    
    LOCAL = "local"
    DEVELOPMENT = "development" 
    STAGING = "staging"
    PRODUCTION = "production"


class AppSettings(BaseSettings):
    """Main application configuration."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application
    app_name: str = Field(default="TGBot Clean Template", description="Application name")
    environment: Environment = Field(default=Environment.LOCAL, description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    secret_key: str = Field(description="Secret key for encryption")
    
    # Database
    database_host: str = Field(default="localhost", description="Database host")
    database_port: int = Field(default=5432, description="Database port") 
    database_name: str = Field(description="Database name")
    database_user: str = Field(description="Database user")
    database_password: str = Field(description="Database password")
    
    # Redis
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")
    redis_password: str | None = Field(default=None, description="Redis password")
    
    # Telegram
    telegram_bot_token: str = Field(description="Telegram bot token")
    telegram_webhook_url: str | None = Field(default=None, description="Webhook URL for production")
    telegram_webhook_secret: str | None = Field(default=None, description="Webhook secret token")
    telegram_use_webhook: bool = Field(default=False, description="Use webhook instead of polling")
    
    # Security
    register_passphrase: str | None = Field(default=None, description="Registration passphrase")
    creator_id: int | None = Field(default=None, description="Bot creator Telegram ID")
    
    # API
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # Scheduler
    scheduler_timezone: str = Field(default="UTC", description="Scheduler timezone")
    daily_digest_time: str = Field(default="09:00", description="Daily digest time (HH:MM)")
    
    @property
    def database_url(self) -> str:
        """Get database URL."""
        return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
    
    @property
    def redis_url(self) -> str:
        """Get Redis URL."""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment in (Environment.LOCAL, Environment.DEVELOPMENT)
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == Environment.PRODUCTION


def get_settings() -> AppSettings:
    """Get application settings."""
    return AppSettings()


def get_database_url() -> str:
    """Get database URL for Alembic."""
    settings = get_settings()
    return settings.database_url 