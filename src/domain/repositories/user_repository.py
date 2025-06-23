"""User repository interface."""
from abc import ABC, abstractmethod
from typing import Sequence

from ..entities.user import User
from ..value_objects.social_id import SocialId
from ..value_objects.user_id import UserId


class UserRepository(ABC):
    """Abstract user repository interface."""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user.
        
        Args:
            user: User entity to create
            
        Returns:
            Created user with assigned ID
            
        Raises:
            UserAlreadyExistsError: If user with same social_id exists
        """
        ...
    
    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> User | None:
        """Get user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            User entity or None if not found
        """
        ...
    
    @abstractmethod
    async def get_by_social_id(self, social_id: SocialId) -> User | None:
        """Get user by social ID.
        
        Args:
            social_id: Social media identifier (e.g., Telegram ID)
            
        Returns:
            User entity or None if not found
        """
        ...
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user.
        
        Args:
            user: User entity to update
            
        Returns:
            Updated user entity
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        ...
    
    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Delete user by ID.
        
        Args:
            user_id: User identifier
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        ...
    
    @abstractmethod
    async def get_all(self, *, limit: int | None = None, offset: int = 0) -> Sequence[User]:
        """Get all users with pagination.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            Sequence of user entities
        """
        ...
    
    @abstractmethod
    async def get_top_by_taps(self, limit: int = 10) -> Sequence[User]:
        """Get top users by tap count.
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            Sequence of user entities ordered by taps descending
        """
        ...
    
    @abstractmethod
    async def count(self) -> int:
        """Get total number of users.
        
        Returns:
            Total user count
        """
        ... 