"""
Интерфейс сервиса приложения для работы с пользователями.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from application.dtos.user_dto import UserDto, UserProfileDto, CreateUserDto
from application.dtos.leaderboard_dto import LeaderboardDto


class UserService(ABC):
    """
    Интерфейс сервиса приложения для работы с пользователями.
    
    Определяет контракт для бизнес-операций с пользователями.
    """
    
    @abstractmethod
    async def register_user(self, create_user_dto: CreateUserDto) -> UserDto:
        """Зарегистрировать нового пользователя."""
        pass
    
    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserDto]:
        """Получить пользователя по ID."""
        pass
    
    @abstractmethod
    async def increment_taps(self, user_id: int) -> Optional[UserDto]:
        """Увеличить количество нажатий пользователя."""
        pass
    
    @abstractmethod
    async def update_profile(
        self, 
        user_id: int, 
        profile_dto: UserProfileDto
    ) -> Optional[UserDto]:
        """Обновить профиль пользователя."""
        pass
    
    @abstractmethod
    async def get_leaderboard(self) -> LeaderboardDto:
        """Получить рейтинг пользователей."""
        pass
    
    @abstractmethod
    async def user_exists(self, user_id: int) -> bool:
        """Проверить существование пользователя."""
        pass 