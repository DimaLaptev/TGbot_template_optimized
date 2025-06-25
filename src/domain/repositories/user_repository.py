"""
Абстракция репозитория для работы с пользователями.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.user import User
from domain.value_objects.user_id import UserId


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
    async def save(self, user: User) -> None:
        """Сохранить пользователя."""
        pass
    
    @abstractmethod
    async def exists(self, user_id: UserId) -> bool:
        """Проверить существование пользователя."""
        pass
    
    @abstractmethod
    async def find_all_ordered_by_taps(self) -> List[User]:
        """Получить всех пользователей, отсортированных по количеству нажатий."""
        pass
    
    @abstractmethod
    async def get_total_taps(self) -> int:
        """Получить общее количество нажатий всех пользователей."""
        pass 