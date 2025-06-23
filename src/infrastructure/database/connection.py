"""Database connection management."""
import structlog
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, create_async_engine
from sqlalchemy.pool import NullPool

from ..config import AppSettings

logger = structlog.get_logger(__name__)


class DatabaseConnectionFactory:
    """Factory for creating database connections."""
    
    def __init__(self, settings: AppSettings) -> None:
        """Initialize database factory.
        
        Args:
            settings: Application configuration
        """
        self._settings = settings
        self._engine: AsyncEngine | None = None
    
    def create_engine(self) -> AsyncEngine:
        """Create database engine.
        
        Returns:
            Async SQLAlchemy engine
        """
        if self._engine is None:
            logger.info("Creating database engine", url=self._settings.database_url.split("@")[1])
            
            self._engine = create_async_engine(
                self._settings.database_url,
                echo=False,  # Set to True for SQL query logging
                pool_pre_ping=True,
                pool_recycle=3600,  # Recycle connections after 1 hour
                connect_args={
                    "server_settings": {
                        "application_name": "tgbot_clean_template",
                    }
                },
            )
        
        return self._engine
    
    async def create_connection(self) -> AsyncConnection:
        """Create database connection.
        
        Returns:
            Async database connection
        """
        engine = self.create_engine()
        return await engine.connect()
    
    async def close(self) -> None:
        """Close database engine."""
        if self._engine:
            logger.info("Closing database engine")
            await self._engine.dispose()
            self._engine = None


class TestDatabaseConnectionFactory(DatabaseConnectionFactory):
    """Factory for test database connections."""
    
    def create_engine(self) -> AsyncEngine:
        """Create test database engine with different settings."""
        if self._engine is None:
            logger.info("Creating test database engine")
            
            self._engine = create_async_engine(
                self._settings.database_url,
                echo=False,
                poolclass=NullPool,  # No connection pooling for tests
                connect_args={
                    "server_settings": {
                        "application_name": "tgbot_test",
                    }
                },
            )
        
        return self._engine 