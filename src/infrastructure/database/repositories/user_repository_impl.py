"""
Реализация репозитория пользователей на основе БД.
"""
from typing import List, Optional

from domain.entities.user import User
from domain.value_objects.user_id import UserId
from domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    """
    Реализация репозитория пользователей с использованием базы данных.
    
    Инкапсулирует детали работы с конкретной СУБД,
    реализует абстракцию из доменного слоя.
    """
    
    def __init__(self, database_connection) -> None:
        """
        database_connection - подключение к БД (будет заменено на SQLAlchemy).
        """
        self._db = database_connection
    
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        """Найти пользователя по ID."""
        # TODO: Реализовать с SQLAlchemy
        # Заглушка для демонстрации архитектуры
        raise NotImplementedError("Будет реализовано с SQLAlchemy")
    
    async def save(self, user: User) -> None:
        """Сохранить пользователя."""
        # TODO: Реализовать с SQLAlchemy
        raise NotImplementedError("Будет реализовано с SQLAlchemy")
    
    async def exists(self, user_id: UserId) -> bool:
        """Проверить существование пользователя."""
        # TODO: Реализовать с SQLAlchemy
        raise NotImplementedError("Будет реализовано с SQLAlchemy")
    
    async def find_all_ordered_by_taps(self) -> List[User]:
        """Получить всех пользователей, отсортированных по количеству нажатий."""
        # TODO: Реализовать с SQLAlchemy
        raise NotImplementedError("Будет реализовано с SQLAlchemy")
    
    async def get_total_taps(self) -> int:
        """Получить общее количество нажатий всех пользователей."""
        # TODO: Реализовать с SQLAlchemy
        raise NotImplementedError("Будет реализовано с SQLAlchemy") 