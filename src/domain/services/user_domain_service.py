"""
Доменный сервис для работы с пользователями.
"""
from typing import List, Optional

from domain.entities.user import User
from domain.value_objects.user_id import UserId
from domain.value_objects.username import Username
from domain.value_objects.user_profile import UserProfile
from domain.repositories.user_repository import UserRepository


class UserDomainService:
    """
    Доменный сервис для работы с пользователями.
    
    Инкапсулирует сложную бизнес-логику, которая не принадлежит
    конкретной сущности, но относится к домену.
    """
    
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository
    
    async def register_user(self, user_id: UserId, username: Username) -> User:
        """Зарегистрировать нового пользователя."""
        if await self._user_repository.exists(user_id):
            raise ValueError(f"Пользователь с ID {user_id} уже существует")
        
        user = User.create_new(user_id, username)
        await self._user_repository.save(user)
        return user
    
    async def increment_user_taps(self, user_id: UserId) -> Optional[User]:
        """Увеличить количество нажатий пользователя."""
        user = await self._user_repository.find_by_id(user_id)
        if user is None:
            return None
        
        user.increment_taps()
        await self._user_repository.save(user)
        return user
    
    async def update_user_profile(
        self, 
        user_id: UserId, 
        profile: UserProfile
    ) -> Optional[User]:
        """Обновить профиль пользователя."""
        user = await self._user_repository.find_by_id(user_id)
        if user is None:
            return None
        
        user.update_profile(profile)
        await self._user_repository.save(user)
        return user
    
    async def get_leaderboard(self) -> List[User]:
        """Получить топ пользователей по количеству нажатий."""
        return await self._user_repository.find_all_ordered_by_taps()
    
    async def calculate_user_position(self, user_id: UserId) -> Optional[int]:
        """Вычислить позицию пользователя в рейтинге."""
        leaderboard = await self.get_leaderboard()
        
        for position, user in enumerate(leaderboard, 1):
            if user.id == user_id:
                return position
        
        return None 