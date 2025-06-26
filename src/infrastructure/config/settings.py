"""
Система конфигурации приложения.
"""
from enum import Enum
from typing import Optional

try:
    # Pydantic v1
    from pydantic import BaseSettings, Field
except ImportError:
    # Pydantic v2
    from pydantic_settings import BaseSettings
    from pydantic import Field


class Environment(str, Enum):
    """Окружения приложения."""
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class DatabaseSettings(BaseSettings):
    """Настройки базы данных."""
    host: str = Field(..., env="POSTGRES_HOST")
    port: int = Field(5432, env="POSTGRES_PORT")
    database: str = Field(..., env="POSTGRES_DB")
    username: str = Field(..., env="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    
    @property
    def url(self) -> str:
        """Получить URL подключения к БД."""
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    class Config:
        env_prefix = ""


class RedisSettings(BaseSettings):
    """Настройки Redis."""
    host: str = Field("localhost", env="FSM_REDIS_HOST")
    port: int = Field(6379, env="FSM_REDIS_PORT")
    db: int = Field(0, env="FSM_REDIS_DB")
    password: Optional[str] = Field(None, env="FSM_REDIS_PASS")
    
    @property
    def url(self) -> str:
        """Получить URL подключения к Redis."""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"
    
    class Config:
        env_prefix = ""


class TelegramSettings(BaseSettings):
    """Настройки Telegram бота."""
    bot_token: str = Field(..., env="TG_BOT_TOKEN")
    creator_id: Optional[int] = Field(None, env="CREATOR_ID")
    register_passphrase: Optional[str] = Field(None, env="REGISTER_PASSPHRASE")
    
    class Config:
        env_prefix = ""


class AppSettings(BaseSettings):
    """Основные настройки приложения."""
    environment: Environment = Field(Environment.LOCAL, env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")
    
    # Database settings - упрощенно
    postgres_host: str = Field("localhost", env="DATABASE_HOST")
    postgres_port: int = Field(5432, env="DATABASE_PORT")
    postgres_db: str = Field("tgbot_db", env="DATABASE_NAME")
    postgres_user: str = Field("tgbot_user", env="DATABASE_USER")
    postgres_password: str = Field("password", env="DATABASE_PASSWORD")
    
    # Redis settings
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")
    redis_password: Optional[str] = Field(None, env="REDIS_PASSWORD")
    
    # Telegram settings
    telegram_bot_token: str = Field("", env="TELEGRAM_BOT_TOKEN")
    telegram_creator_id: Optional[int] = Field(None, env="CREATOR_ID")
    telegram_register_passphrase: Optional[str] = Field(None, env="REGISTER_PASSPHRASE")
    
    @property
    def database_url(self) -> str:
        """Получить URL подключения к БД."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def redis_url(self) -> str:
        """Получить URL подключения к Redis."""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    class Config:
        env_file = "../.env"  # Путь относительно src папки
        env_nested_delimiter = "__"
        extra = "ignore"  # Игнорируем дополнительные поля из .env


def get_settings() -> AppSettings:
    """Получить настройки приложения."""
    return AppSettings() 