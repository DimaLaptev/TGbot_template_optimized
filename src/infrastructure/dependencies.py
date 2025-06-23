"""Dependency injection container."""
from typing import AsyncContextManager, TypeVar
import structlog
from contextlib import asynccontextmanager

from ..application.use_cases.user_use_cases import UserUseCases
from ..domain.repositories.unit_of_work import UnitOfWork
from .config import AppSettings, get_settings
from .database.connection import DatabaseConnectionFactory
from .database.unit_of_work_impl import SQLAlchemyUnitOfWork

logger = structlog.get_logger(__name__)

T = TypeVar("T")


class Container:
    """Simple dependency injection container."""
    
    def __init__(self, settings: AppSettings | None = None) -> None:
        """Initialize container.
        
        Args:
            settings: Application settings (optional, will load from env if not provided)
        """
        self._settings = settings or get_settings()
        self._db_factory: DatabaseConnectionFactory | None = None
        self._instances: dict[type, any] = {}
        
        logger.info("Initializing dependency container", environment=self._settings.environment)
    
    @property
    def settings(self) -> AppSettings:
        """Get application settings."""
        return self._settings
    
    def get_database_factory(self) -> DatabaseConnectionFactory:
        """Get database connection factory."""
        if self._db_factory is None:
            self._db_factory = DatabaseConnectionFactory(self._settings)
        return self._db_factory
    
    @asynccontextmanager
    async def get_uow(self) -> AsyncContextManager[UnitOfWork]:
        """Get Unit of Work instance.
        
        Yields:
            Unit of Work instance within a database connection context
        """
        db_factory = self.get_database_factory()
        
        async with await db_factory.create_connection() as connection:
            uow = SQLAlchemyUnitOfWork(connection)
            yield uow
    
    async def get_user_use_cases(self) -> UserUseCases:
        """Get user use cases instance.
        
        Returns:
            UserUseCases instance with injected dependencies
        """
        # For this simple case, we'll create a new instance each time
        # In a more complex app, you might want to implement proper singleton pattern
        async with self.get_uow() as uow:
            return UserUseCases(uow)
    
    def register_instance(self, type_: type[T], instance: T) -> None:
        """Register a singleton instance.
        
        Args:
            type_: Type to register
            instance: Instance to register
        """
        self._instances[type_] = instance
        logger.debug("Registered instance", type=type_.__name__)
    
    def get_instance(self, type_: type[T]) -> T:
        """Get registered instance.
        
        Args:
            type_: Type to get
            
        Returns:
            Registered instance
            
        Raises:
            KeyError: If type is not registered
        """
        if type_ not in self._instances:
            raise KeyError(f"Instance of type {type_.__name__} not registered")
        return self._instances[type_]
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up container resources")
        
        if self._db_factory:
            await self._db_factory.close()
        
        self._instances.clear()


# Global container instance
_container: Container | None = None


def get_container(settings: AppSettings | None = None) -> Container:
    """Get global container instance.
    
    Args:
        settings: Optional settings override
        
    Returns:
        Global container instance
    """
    global _container
    
    if _container is None or settings is not None:
        _container = Container(settings)
    
    return _container


async def cleanup_container() -> None:
    """Clean up global container."""
    global _container
    
    if _container:
        await _container.cleanup()
        _container = None 