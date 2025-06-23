"""Unit of Work implementation with SQLAlchemy."""
from typing import Any

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncTransaction

from ...domain.repositories.unit_of_work import UnitOfWork
from .repositories.user_repository_impl import SQLAlchemyUserRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy implementation of Unit of Work."""
    
    def __init__(self, connection: AsyncConnection) -> None:
        """Initialize Unit of Work with database connection.
        
        Args:
            connection: Database connection
        """
        self._connection = connection
        self._transaction: AsyncTransaction | None = None
        self.users = SQLAlchemyUserRepository(connection)
    
    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        """Start a transaction."""
        self._transaction = await self._connection.begin()
        return self
    
    async def __aexit__(self, exc_type: type, exc_val: Any, exc_tb: Any) -> None:
        """End transaction - commit if no exception, rollback otherwise."""
        if self._transaction:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        if self._transaction:
            await self._transaction.commit()
            self._transaction = None
    
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        if self._transaction:
            await self._transaction.rollback()
            self._transaction = None 