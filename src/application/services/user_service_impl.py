"""
Реализация сервиса приложения для работы с пользователями.
"""
from typing import List, Optional

from application.interfaces.user_service import UserService
from application.dtos.user_dto import UserDto, UserProfileDto, CreateUserDto
from application.dtos.leaderboard_dto import LeaderboardDto, LeaderboardEntryDto

from domain.entities.user import User
from domain.value_objects.user_id import UserId
from domain.value_objects.username import Username
from domain.value_objects.user_profile import UserProfile
from domain.services.user_domain_service import UserDomainService


class UserServiceImpl(UserService):
    """
    Реализация сервиса приложения для работы с пользователями.
    
    Координирует взаимодействие между доменным слоем и внешними слоями,
    преобразует DTO в доменные объекты и обратно.
    """
    
    def __init__(self, user_domain_service: UserDomainService) -> None:
        self._user_domain_service = user_domain_service
    
    async def register_user(self, create_user_dto: CreateUserDto) -> UserDto:
        """Зарегистрировать нового пользователя."""
        user_id = UserId(create_user_dto.user_id)
        username = Username(create_user_dto.username)
        
        user = await self._user_domain_service.register_user(user_id, username)
        return self._map_user_to_dto(user)
    
    async def get_user(self, user_id: int) -> Optional[UserDto]:
        """Получить пользователя по ID."""
        domain_user_id = UserId(user_id)
        user = await self._user_domain_service._user_repository.find_by_id(domain_user_id)
        
        if user is None:
            return None
        
        return self._map_user_to_dto(user)
    
    async def increment_taps(self, user_id: int) -> Optional[UserDto]:
        """Увеличить количество нажатий пользователя."""
        domain_user_id = UserId(user_id)
        user = await self._user_domain_service.increment_user_taps(domain_user_id)
        
        if user is None:
            return None
        
        return self._map_user_to_dto(user)
    
    async def update_profile(
        self, 
        user_id: int, 
        profile_dto: UserProfileDto
    ) -> Optional[UserDto]:
        """Обновить профиль пользователя."""
        domain_user_id = UserId(user_id)
        domain_profile = UserProfile(
            name=profile_dto.name,
            info=profile_dto.info,
            photo_id=profile_dto.photo_id
        )
        
        user = await self._user_domain_service.update_user_profile(
            domain_user_id, 
            domain_profile
        )
        
        if user is None:
            return None
        
        return self._map_user_to_dto(user)
    
    async def get_leaderboard(self) -> LeaderboardDto:
        """Получить рейтинг пользователей."""
        users = await self._user_domain_service.get_leaderboard()
        total_taps = await self._user_domain_service._user_repository.get_total_taps()
        
        entries = [
            LeaderboardEntryDto(
                position=position,
                user=self._map_user_to_dto(user)
            )
            for position, user in enumerate(users, 1)
        ]
        
        return LeaderboardDto(entries=entries, total_taps=total_taps)
    
    async def user_exists(self, user_id: int) -> bool:
        """Проверить существование пользователя."""
        domain_user_id = UserId(user_id)
        return await self._user_domain_service._user_repository.exists(domain_user_id)
    
    def _map_user_to_dto(self, user: User) -> UserDto:
        """Преобразовать доменного пользователя в DTO."""
        profile_dto = None
        if user.profile is not None:
            profile_dto = UserProfileDto(
                name=user.profile.name,
                info=user.profile.info,
                photo_id=user.profile.photo_id
            )
        
        return UserDto(
            id=user.id.value,
            username=user.username.value,
            registration_date=user.registration_date,
            taps=user.taps,
            profile=profile_dto
        ) 