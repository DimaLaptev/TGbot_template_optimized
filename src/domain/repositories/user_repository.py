"""
Абстракция репозитория для работы с пользователями.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.user import User
from domain.value_objects.user_id import UserId
from domain.value_objects.username import Username


class UserRepository(ABC):
    """
    Абстракция репозитория для работы с пользователями.
    
    Определяет интерфейс для работы с хранилищем пользователей,
    следуя принципу Dependency Inversion.
    """
    
    @abstractmethod
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        """Найти пользователя по ID."""
        pass
    
    @abstractmethod
    async def find_by_username(self, username: Username) -> Optional[User]:
        """Найти пользователя по username."""
        pass
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Сохранить пользователя и вернуть обновленную сущность."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UserId) -> bool:
        """Удалить пользователя. Возвращает True если удален."""
        pass
    
    @abstractmethod
    async def find_top_users(self, limit: int = 10) -> List[User]:
        """Найти топ пользователей по количеству нажатий."""
        pass 