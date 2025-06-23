"""Unit of Work pattern interface."""
from abc import ABC, abstractmethod
from typing import Any

from .user_repository import UserRepository


class UnitOfWork(ABC):
    """Abstract Unit of Work for managing transactions."""
    
    users: UserRepository
    
    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        """Start a transaction."""
        ...
    
    @abstractmethod
    async def __aexit__(self, exc_type: type, exc_val: Any, exc_tb: Any) -> None:
        """End transaction - commit if no exception, rollback otherwise."""
        ...
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        ...
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        ... 